import os

import sys

sys.path.append('lib')
from flask import Flask, send_from_directory

import cirrocumulus
from cirrocumulus.cloud_firestore import CloudFireStore
from cirrocumulus.api import cirro_blueprint
from cirrocumulus.envir import CIRRO_AUTH_CLIENT_ID, CIRRO_AUTH, CIRRO_DATABASE, CIRRO_DATASET_PROVIDERS
from cirrocumulus.google_auth import GoogleAuth
from cirrocumulus.no_auth import NoAuth
from cirrocumulus.util import add_dataset_providers

client_path = os.path.join(cirrocumulus.__path__[0], 'client')
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.


app = Flask(__name__, static_folder=client_path, static_url_path='')
app.register_blueprint(cirro_blueprint, url_prefix='/api')


@app.route('/')
def root():
    return send_from_directory(client_path, "index.html")


if os.environ.get(CIRRO_AUTH_CLIENT_ID) is not None:
    app.config[CIRRO_AUTH] = GoogleAuth()
else:
    app.config[CIRRO_AUTH] = NoAuth()

app.config[CIRRO_DATABASE] = CloudFireStore()
os.environ[CIRRO_DATASET_PROVIDERS] = ','.join(['cirrocumulus.zarr_dataset.ZarrDataset',
                                                'cirrocumulus.parquet_dataset.ParquetDataset'])
add_dataset_providers()
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
