from flask import Flask
import os
import googleapiclient.discovery

app = Flask(__name__)

developer_key = os.environ.get('DEVELOPER_KEY')
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)

from app import routes
