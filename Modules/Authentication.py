import os
import adal
import requests
import logging
import keyring
import json
from datetime import datetime, time

class Authentication:
    if os.path.isfile(".\\Config.json"):
        with open(".\\Config.json") as config_json:
            config_contents = json.load(config_json)
    else:
        os.chdir("..")
        if os.path.isfile(".\\Config.json"):
            with open(".\\Config.json") as config_json:
                config_contents = json.load(config_json)
        else:
            print("Configuration file Config.json missing. Exiting program.")
            time.sleep(10)
            exit()

    testing = config_contents['Testing']

    if testing:
        username = config_contents['Test_Username']
        tenant_id = config_contents['Test_Tenant_ID']
        client_id = config_contents['Test_Client_ID']
        password = keyring.get_password("Test_Email2Slack", username)
    else:
        username = config_contents['Username']
        tenant_id = config_contents['Tenant_ID']
        client_id = config_contents['Client_ID']
        password = keyring.get_password("Email2Slack", username)

    authority = config_contents['Authority'] + tenant_id
    resource = config_contents['Resource']
    graph_api_endpoint = config_contents['Graph_API_Endpoint']

    def get_access_token(self):
        try:
            context = adal.AuthenticationContext(self.authority)

            token = context.acquire_token_with_username_password(
                self.resource,
                self.username,
                self.password,
                self.client_id
            )

            return token
        except Exception as error:
            logging.error(f"Error encountered while acquiring authentication token. Error: {error}")
            raise error

    def form_header(self):
        token = self.get_access_token()

        headers = {
            'Authorization' : f'Bearer {token["accessToken"]}',
            'Accept' : 'application/json',
            'Content-Type' : 'application/json'
        }

        return headers