import requests
import json

# find the assay id for a specific assay
def get_sbol_from_uri(URI):
    get_sbol_from_uri = URI
    headers = {
        'Accept': 'text/plain'
    }
    return requests.get(get_sbol_from_uri, headers=headers)

#def sbh_login():
    #sbh_request_login_url = "https://synbiohub.org/login"
    #payload = {'email': "saisam17@gmail.com", 'password': 'Il0vem$her1776'}
    #return requests.post(sbh_request_login_url, data=payload)

