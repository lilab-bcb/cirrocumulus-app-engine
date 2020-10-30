import os

from flask import Flask, send_from_directory

import cirrocumulus
from cirrocumulus.api import blueprint, auth_api, database_api, dataset_api
from cirrocumulus.envir import CIRRO_AUTH_CLIENT_ID
from cirrocumulus.firestore_datastore import FirestoreDatastore
from cirrocumulus.google_auth import GoogleAuth
from cirrocumulus.no_auth import NoAuth
from cirrocumulus.parquet_dataset import ParquetDataset


client_path = os.path.join(cirrocumulus.__path__[0], 'client')
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.


app = Flask(__name__, static_folder=client_path, static_url_path='')
app.register_blueprint(blueprint, url_prefix='/api')


@app.route('/')
def root():
    return send_from_directory(client_path, "index.html")


dataset_api.add(ParquetDataset())

if os.environ.get(CIRRO_AUTH_CLIENT_ID) is not None:
    auth_api.provider = GoogleAuth(os.environ.get(CIRRO_AUTH_CLIENT_ID))
else:
    auth_api.provider = provider = NoAuth()
database_api.provider = FirestoreDatastore()

if __name__ == '__main__':
    # from flask_cors import CORS
    # CORS(app)
    app.run(host='127.0.0.1', port=5000, debug=True)
