import uuid

from flask import Flask, request, abort
import os, flask
import sys
import traceback
import logging
import authentication_util
import model_util
import sbh_util
import html_creator as hc
import matplotlib.pyplot as plt
import uuid
import sbol2
from Measurement import Measurement

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route("/status")
def status():
    return("The Visualisation Test Plugin Flask Server is up and running")


@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json(force=True)
    rdf_type = data['type']

    # ~~~~~~~~~~~~ REPLACE THIS SECTION WITH OWN RUN CODE ~~~~~~~~~~~~~~~~~~~
    # uses rdf types
    accepted_types = {'ExperimentalData'}

    acceptable = rdf_type in accepted_types

    # # to ensure it shows up on all pages
    # acceptable = True
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~ END SECTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if acceptable:
        return f'The type sent ({rdf_type}) is an accepted type', 200
    else:
        return f'The type sent ({rdf_type}) is NOT an accepted type', 415


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json(force=True)

    top_level_url = data['top_level']
    complete_sbol = data['complete_sbol']
    instance_url = data['instanceUrl']
    size = data['size']
    rdf_type = data['type']
    shallow_sbol = data['shallow_sbol']

    url = complete_sbol.replace('/sbol', '')

    cwd = os.getcwd()
    filename = os.path.join(cwd, "Flapjack.html")

    try:
        doc = sbol2.Document()
        doc.read(complete_sbol)
        app.logger.info(str(complete_sbol))
        #doc.write()

        sample_ids = []
        for ed in doc.experimentalData:
            sample_sbol = ed.properties['http://flapjack.rudge-lab.org/sample']
            for sample_sbol_id in sample_sbol:
                app.logger.info("sample is: " + str(sample_sbol_id))
                sample_ids.append(str(sample_sbol_id))
        app.logger.info(print(sample_ids))

        #make a request out to flapjack on localhost
        #make login request
        flapjack_log_in_response = authentication_util.flapjack_login_request()

        if flapjack_log_in_response.status_code == 200: # if successful login, make a get studies request
            access_token = flapjack_log_in_response.json()["access"]
            app.logger.info(access_token)
            #new functions will be called from here
            app.logger.info("successfully logged in")

            #sample_measurements = [] #[sample_id : List<Measurement>]
            #for sample_id in sample_ids:
            for sample_id in sample_ids:
                m_set = []

                flapjack_get_measurements_response = model_util.flapjack_get_measurements_for_sample_request(sample_id, access_token)
                for measurement in flapjack_get_measurements_response.json()["results"]:
                    m_id = measurement["id"]
                    m_value = measurement["value"]
                    m_time = measurement["time"]
                    m_signal = measurement["signal"]
                    m_set.append(Measurement(m_id, m_value, m_time, m_signal, sample_id))

                signal_measurements_dict = {}

                for measurement in m_set:
                    signal = measurement.getSignal()
                    if signal not in signal_measurements_dict:
                        m_list = [measurement]
                        signal_measurements_dict[signal] = m_list
                    else:
                        signal_measurements_dict[signal].append(measurement)

                #dict : dicts : lists --> {sample : {sig1 : [Measusrements], sign2 : [Measurements]}}
                figTitleArr = []
                for signal_measurement in signal_measurements_dict.values():
                    time = []
                    values = []
                    for m in signal_measurement:
                        time.append(m.getTime())
                        values.append(m.getValue())
                    plt.scatter(time, values)
                    plt.xlabel("time")
                    plt.ylabel("values")
                    plt.title("sample: " + str(sample_id) + ", signal: " + str(signal_measurement[0].getSignal()))
                    rand_hash = str(uuid.uuid4())
                    fig_title = rand_hash + ".jpg"
                    figTitleArr.append(fig_title)
                    app.logger.info(fig_title)
                    plt.savefig(fig_title)

# save figTitles into array
#pass items from array into img src

            #TODO call websockets to plot

        # Plot creation
        signal_names = ['GFP', 'RFP', 'YFP', 'CFP']
        signal_graphs = ['<div>GFP</div>', '<div>RFP</div>', '<div>YFP</div>', '<div>CFP</div>']
        all_graph = "<div>Original</div>"
        html_file = hc.html_creator(signal_names, signal_graphs, all_graph)

            #html_output = authentication_util.plot(figname)
        return html_file
        # TODO error handling -- if authentiation fails and or any of the calls fail, we need graceful handling
        # TODO Testing, unit + manual
        # TODO documentation
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        lnum = exc_tb.tb_lineno
        abort(400, f'Exception is: {e}, exc_type: {exc_type}, exc_obj: {exc_obj}, fname: {fname}, line_number: {lnum}, traceback: {traceback.format_exc()}')