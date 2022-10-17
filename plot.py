from flask import Flask, request, abort
import os
import sys
import traceback
import logging
#import authentication_util
import model_util
import math
import sbh_util
import matplotlib.pyplot as plt
import uuid
import sbol2
from Measurement import Measurement
import plotly.express as px
from base64 import b64encode
import io
import pandas as pd
from flapjack import Flapjack

# Parse sbol to obtain hashmap of sample id

#direct = __file__
#test_file_path = os.path.join(os.path.split(os.path.split(direct)[0])[0],
                              #'tests', 'test_files')
#file_path_out = os.path.join(test_file_path, 'Sample2.xml')
doc = "C:/Users/saisa/Plugin-Visual-Test/tests/test_files/Sample1.xml"
file_path_out = doc
doc = sbol2.Document()
doc.read(file_path_out)

#FJ Login

# flapjack_log_in_response = authentication_util.flapjack_login_request()
# access_token = flapjack_log_in_response.json()["access"]

fj_url = "flapjack.rudge-lab.org:8000" #Web Instance
fj_user = "saisam17"
fj_pass = "Il0vem$her"

fj = Flapjack(url_base=fj_url) #Local Instance
fj.log_in(username=fj_user, password=fj_pass)
access_token = fj.access_token
# if flapjack_log_in_response.status_code == 200: # if successful login, make a get studies request
#
#     app.logger.info(access_token)
#     #new functions will be called from here
#     app.logger.info("successfully logged in")

#Obtain Sample ID

sample_ids = []
for ed in doc:
    #print (ed.properties)
    sample_id = ed.properties['https://flapjack.rudge-lab.org/ID']
    sample_id = str(sample_id[0]).split("/")[-1]
    sample_ids.append(sample_id)

#Obtain measurements by Signal

for sample_id in sample_ids:
    m_set = []
    #print(sample_id)
    flapjack_get_measurements_response = model_util.flapjack_get_measurements_for_sample_request(sample_id,
                                                                                                 access_token)
    #put m_id, m_value, m_time, m_signal into a dataframe and can do in a single line so we can elimiate lines 52-61

    id = []
    time = []  # values
    values = []
    signal = []
    for measurement in flapjack_get_measurements_response.json()["results"]:
        #print(flapjack_get_measurements_response.json())
        id.append(measurement["id"])
        time.append(measurement["time"])
        signal.append(measurement["signal"])
        values.append(measurement["value"])

    d = {}
    d['time'] = time
    d['id'] = id
    d['value'] = values
    d['signal'] = signal
    signal_set = set(signal)
    signal_lookup = {}
    for sig in signal_set:
        flapjack_get_signal_request = model_util.flapjack_get_signal_request(sig, access_token)
        signal_lookup[sig] =flapjack_get_signal_request.json()['results'][0]['name']
    signal_names = [signal_lookup[x] for x in signal]
    d['signal_names'] = signal_names
    df = pd.DataFrame(data=d)
    y_max_val = df['value'].max()
    y_max_val = math.ceil(y_max_val)
    print('this is the max', y_max_val)
    # print(df)
    #print(df)
    #m_set.append(Measurement(m_id, m_value, m_time, m_signal, sample_id)) #maybe able to remove, use dataframe

    #signal_measurements_dict = {} #maybe able to remove

    #for measurement in m_set:
        #signal = measurement.getSignal() #maybe able to remove
        #if signal not in signal_measurements_dict:
            #m_list = [measurement] #maybe able to remove
            #signal_measurements_dict[signal] = m_list #maybe able to remove
        #else:
            #signal_measurements_dict[signal].append(measurement) #maybe able to remove

    # dict : dicts : lists --> {sample : {sig1 : [Measusrements], sign2 : [Measurements]}}
    figTitleArr = []
    #for signal_measurement in signal_measurements_dict.values():
        #time = []
        #values = []
        #signal = []
        #for m in signal_measurement:
            #time.append(m.getTime())
            #values.append(m.getValue())
            #signal.append(m.getValue())
            #df=px.data.iris()
            #print (df)
        # fig = px.scatter(df, x="time", y="values", color="signal")
        #Add parameter range (force axis limits for x and y) fig.update_yaxes(range=[0,ymax]) calculate ymax.
    fig = px.scatter(df, x="time", y="value", color="signal_names", hover_data=[df.index], range_y=[0,y_max_val]) #try to add a legend
    fig.show()
        #nest another for loop in here to do a plot by signal
        # fig.show()
    # px.title("sample: " + str(sample_id) + ", signal: " + str(signal_measurement[0].getSignal()))
    # rand_hash = str(uuid.uuid4())
    # fig_title = rand_hash + ".jpg"
    # figTitleArr.append(fig_title)
    # app.logger.info(fig_title)
        #pull html from figure (plotly, the output can easily be pulled as an html) write it to some path and read in the html again
        #create outputs as inputs for the html creator (Provide as html string, list of signal names (GFP etc), list of html of the graphs for each signal individually)

    # fig_html = fig.write_html("path/to/file.html", full_html=False, include_plotlyjs='cdn')
    for sig in signal_set:
        df_sig = df[df["signal"] == sig]
        df_sig = df_sig.reset_index()
        fig = px.scatter(df_sig, x="time", y="value", hover_data=[df_sig.index], range_y=[0,y_max_val])  # try to add a legend
        fig.show()
















                #for sample_sbol_id in sample_sbol:
                    #app.logger.info("sample is: " + str(sample_sbol_id))
                    #sample_ids.append(str(sample_sbol_id))
            #app.logger.info(print(sample_ids))
