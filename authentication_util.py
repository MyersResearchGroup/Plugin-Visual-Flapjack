import os
import requests

## TODO see if i still need this
def output(flapjack_response):
    cwd = os.getcwd()
    filename = os.path.join(cwd, "Flapjack.html")
    with open(filename, 'r') as htmlfile:
        result = htmlfile.read()

        # put in the url, uri, and instance given by synbiohub
        result = result.replace("FLAPJACK_REQUEST_RESPONSE", str(flapjack_response))
    return result

def status(FLAPJACK_STATUS):
    cwd = os.getcwd()
    filename = os.path.join(cwd, "Flapjack.html")
    with open(filename, 'r') as htmlfile:
        result = htmlfile.read()

        # put in the url, uri, and instance given by synbiohub
        result = result.replace("FLAPJACK_STATUS", str(FLAPJACK_STATUS))
    return result


def plot(FLAPJACK_PLOT):
    cwd = os.getcwd()
    filename = os.path.join(cwd, "Flapjack.html")
    with open(filename, 'r') as htmlfile:
        result = htmlfile.read()

        # put in the url, uri, and instance given by synbiohub
        #result = result.replace("FLAPJACK_PLOT", str(FLAPJACK_PLOT))
    return result


def flapjack_login_request():
    flapjack_request_login_url = "http://3.128.232.8:8000/api/auth/log_in/"
    payload = {'username': "saisam17", 'password': 'Il0vem$her'}
    return requests.post(flapjack_request_login_url, data=payload)


def flapjack_refresh_request(refresh_token):
    flapjack_refresh_request_url = "http://3.128.232.8:8000/api/auth/refresh/"
    payload = {'refresh': refresh_token}
    return requests.post(flapjack_refresh_request_url, data=payload)  # make a refresh request