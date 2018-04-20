import os
import sys
import json
import requests
import logging
import html2text
from datetime import datetime, time

from Modules.Authentication import Authentication
import Modules.APICallers as APICallers
import Modules.SlackTools as SlackTools
from Modules.SlackTools import SlackColors, SlackClient, Attachment
from Modules.EmailClass import EmailObject


# Change current path to where program lives
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

# Load config
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

# Date setup
current_date = datetime.today()
formatted_date = f"{current_date.year}-{current_date.month}-{current_date.day}"

# Log setup
log_location = config_contents['Log_Location']

log_file_name = f"Email2Slack-{formatted_date}.log"

if not os.path.isdir(log_location):
    os.mkdir(log_location)

if not os.path.isfile(os.path.join(log_location, log_file_name)):
    open(os.path.join(log_location, log_file_name), 'a').close()

# Logging Setup
    # Log Levels for reference:
    #     CRITICAL = 50
    #     FATAL = CRITICAL
    #     ERROR = 40
    #     WARNING = 30
    #     WARN = WARNING
    #     INFO = 20
    #     DEBUG = 10
    #     NOTSET = 0

logging.basicConfig(
    format='[ %(asctime)s | %(levelname)s ] %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename=os.path.join(
        log_location,
        log_file_name
    ),
    level=config_contents['Log_Level']
)
logging.getLogger().addHandler(logging.StreamHandler())
logging.info("Log initialized.")

graph_api_endpoint = config_contents['Graph_API_Endpoint']
testing = config_contents['Testing']
username = config_contents['Username']
slack_access = "Slack WebHook Goes Here"  # Production

if testing:
    slack_access = "Test Slack WebHook Goes Here" # Test
    username = config_contents['Test_Username']

slack_client = SlackClient(slack_access)

try:

    authentication = Authentication()

    token = authentication.get_access_token()

    headers = {
        'Authorization' : f'Bearer {token["accessToken"]}',
        'Accept' : 'application/json',
        'Content-Type' : 'application/json'
    }

    mail_folders = APICallers.Get_API_Results(
        graph_api_endpoint,
        f"/users/{username}/mailFolders",
        headers
    )

    if mail_folders is not None:
        for mail_folder in mail_folders:
            if mail_folder['displayName'] == "Inbox":
                inbox_mail_folder_id = mail_folder['id']
            elif mail_folder['displayName'] == "Archive":
                archive_mail_folder_id = mail_folder['id']

        email_json_data = APICallers.Get_API_Results(
            graph_api_endpoint,
            f"/users/{username}/mailFolders/{inbox_mail_folder_id}/messages?$filter=isRead eq false",
            headers
        )

        if email_json_data != []:
            for email in email_json_data:
                email_object = EmailObject(
                    email['bodyPreview'],
                    email['subject'],
                    email['sentDateTime'],
                    email['body']['content'],
                    email['sender']['emailAddress']['address'],
                    email['id']
                )

                mark_down = html2text.html2text(email_object.Email_Body_Html)

                slack_color = None
                slack_channel = ""

                sending_email_addresses = config_contents['Sending_Email_Addresses']
                for sender_key in sending_email_addresses.keys():
                    if testing:
                        if email_object.Email_Sent_From == sender_key:
                            slack_color = getattr(SlackColors, sending_email_addresses[sender_key]['slack_color'])
                        else:
                            slack_color = SlackColors.White
                    else:
                        if email_object.Email_Sent_From == sender_key:
                            slack_color = getattr(SlackColors, sending_email_addresses[sender_key]['slack_color'])
                            slack_channel = sending_email_addresses[sender_key]['slack_channel']
                        else:
                            slack_color = SlackColors.White

                attachment = Attachment(
                    text=mark_down.replace("**","*"),
                    color=slack_color,
                    pretext=f"`{email_object.Email_Subject}` sent on *{email_object.Email_Sent_DateTime.strftime('%m-%d-%Y')}* at *{email_object.Email_Sent_DateTime.strftime('%X')} EST*"
                )

                post_message = slack_client.Post_Message(
                    channel=slack_channel,
                    username="Email2Slack Alerts",
                    attachments=attachment
                )

                if post_message:
                    APICallers.Mark_As_Read(
                        graph_api_endpoint,
                        username,
                        email_object.Email_ID,
                        headers
                    )

                    APICallers.Move_Email(
                        archive_mail_folder_id,
                        graph_api_endpoint,
                        username,
                        email_object.Email_ID,
                        headers
                    )
                else:
                    logging.info("Failed to post message. Leaving it unread and in Inbox.")

except Exception as error:
    error_attachment = Attachment(
        text=error,
        color=SlackColors.Purple,
        pretext="*Program Exception - Halting service*"
    )

    slack_client.Post_Message(
        username="Email2Slack Alerts",
        attachments=error_attachment
    )

    logging.error(f"Unhandled Exception: {error}")

logging.info("Complete")