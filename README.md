# Plugin-Visual-Flapjack
A very plugin to visualize measurement data associated with experimental data (flapjack samples) stored in synbiohub.

# Install
## Using docker
Run `docker run --publish 8103:5000 --detach --name python-fj-plug synbiohub/plugin-visual-flapjack:snapshot`
Check it is up using localhost:8103.

## Using Python
Run `pip install -r requirements.txt` to install the requirements. Then run `FLASK_APP=app python -m flask run`. A flask module will run at localhost:5000/.
