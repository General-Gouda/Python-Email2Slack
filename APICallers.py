import requests
import logging
import json

def Get_API_Results(graph_api_endpoint, location, headers):
    api_url = graph_api_endpoint + location

    continue_code = True

    try:
        api_response = requests.get(url=api_url, headers=headers)
    except Exception as error:
        logging.error(f"API Get Caller exception: {error}")
        continue_code = False

    if continue_code is True:
        api_json_data = api_response.json()
        values = api_json_data['value']
        return values
    else:
        return continue_code

def Api_Action_Caller(graph_api_endpoint, location, call_type, headers, json=None):
    api_url = graph_api_endpoint + location

    continue_code = True

    try:
        if call_type is "post":
            api_response = requests.post(
                url=api_url, headers=headers, json=json
            )
        elif call_type is "patch":
            api_response = requests.patch(
                url=api_url, headers=headers, json=json
            )
    except Exception as error:
        logging.error(f"API Post Caller exception: {error}")
        continue_code = False

    if continue_code:
        api_json_data = api_response.json()

        return api_json_data
    else:
        return False

def Move_Email(archive_mail_folder_id, graph_api_endpoint, username, email_id, headers):
    move_email_body = {
        'DestinationId': archive_mail_folder_id
    }

    try:
        Api_Action_Caller(
            graph_api_endpoint,
            f"/users/{username}/messages/{email_id}/move",
            "post",
            headers,
            move_email_body
        )

        return True
    except Exception:
        return False

def Mark_As_Read(graph_api_endpoint, username, emailID, headers):
    mark_as_read_body = {
        'isRead': True
    }

    try:
        Api_Action_Caller(
            graph_api_endpoint,
            f"/users/{username}/messages/{emailID}",
            "patch",
            headers,
            mark_as_read_body
        )

        return True
    except Exception:
        return False
