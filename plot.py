import math
import sbol2
import os
import plotly.express as px
import tempfile
import requests
import pandas as pd


def create_signal_graphs(file_path_in, fj_access_token):
    # flapjack base url
    fj_url = "flapjack.rudge-lab.org:8000" #Web Instance

    # temporary directory to write intermediate files to
    temp_dir = tempfile.TemporaryDirectory()
    file_out_path = os.path.join(temp_dir.name, 'temp.html')

    # create header for fj requests
    headers = {'Authorization': 'Bearer ' + fj_access_token} # set to give auth token for later requests

    # pull all the sample ids from the document
    doc = sbol2.Document()
    doc.read(file_path_in)
    sample_ids = []
    for ed in doc:
        if 'https://flapjack.rudge-lab.org/ID' in ed.properties:
            sample_id = ed.properties['https://flapjack.rudge-lab.org/ID']
            sample_id = str(sample_id[0]).split("/")[-1]
            sample_ids.append(sample_id)
        else:
            raise ValueError("There were no flapjack IDs associated with this experimental data object")

    for sample_id in sample_ids:
        # pull all of the measurements for a sample
        flapjack_request_measurements_url = f"http://{fj_url}/api/measurement/?sample={str(sample_id)}"
        measurements_list = requests.get(flapjack_request_measurements_url, headers=headers).json()['results']

        # initialise lists
        id = []
        time = []
        values = []
        signal = []

        if len(measurements_list) == 0:
            raise ValueError(f"There are no measurements associated with this sample (id:{sample_id})")

        # pull information into list
        for measurement in measurements_list:
            id.append(measurement["id"])
            time.append(measurement["time"])
            signal.append(measurement["signal"])
            values.append(measurement["value"])

        # create nested dictionary
        d = {}
        d['Time'] = time
        d['id'] = id
        d['Value'] = values
        d['signal_ids'] = signal

        # create a set of signals (list with no repeats)
        signal_set = set(signal)
        signal_lookup = {}
        for sig in signal_set:
            # pull signal name from signal id
            fj_request_signal_url = f"http://{fj_url}/api/signal/?id={str(sig)}"
            fj_signal_response = requests.get(fj_request_signal_url, headers=headers)
            signal_lookup[sig] = fj_signal_response.json()['results'][0]['name']
        signal_names = [signal_lookup[x] for x in signal]

        # add signal names to the dictionary
        d['Signals'] = signal_names

        # turn the dictionary into a dataframe
        df = pd.DataFrame(data=d)

        # calculate the max and min values
        y_max_val = math.ceil(df['Value'].max())
        y_min_val = math.floor(df['Value'].min())
        x_max_val = math.ceil(df['Time'].max())
        x_min_val = math.floor(df['Time'].min())
        if x_min_val >= 0:
            x_min_val = 0
        if y_min_val >= 0:
            y_min_val = 0


        fig = px.scatter(df, x="Time", y="Value", color="Signals", hover_data=[df.index], range_y=[y_min_val,y_max_val], range_x=[x_min_val, x_max_val]) #try to add a legend
        fig.write_html(file_out_path, full_html=False, include_plotlyjs='cdn')
        with open(file_out_path, 'r') as f:
                all_graph = f.read()
        # fig.show()

        # create plot for every signal
        signal_names = []
        signal_plots = []
        color_list = px.colors.qualitative.Plotly
        num_colors = len(color_list)
        for ind, sig in enumerate(signal_set):
            # filter data frame by signal
            df_sig = df[df["signal_ids"] == sig]
            df_sig = df_sig.reset_index()

            # add signal names to list
            signal_names.append(df_sig['Signals'][0])

            # create figure html 
            col_ind = ind % num_colors # ensures cycles through list if there are more than the number of possible colours
            fig = px.scatter(df_sig, x="Time", y="Value", hover_data=[df_sig.index], range_y=[y_min_val,y_max_val], range_x=[x_min_val, x_max_val])
            fig.update_traces(marker=dict(color=color_list[col_ind])) # make sure the markers match the colour from the overview plot
            fig.write_html(file_out_path, full_html=False, include_plotlyjs='cdn')
            with open(file_out_path, 'r') as f:
                signal_plots.append(f.read())
            # fig.show()
    return (signal_names, signal_plots, all_graph)