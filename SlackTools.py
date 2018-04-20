import requests

class SlackClient:
    def __init__(self, urlWithAccessToken):
        self._uri = urlWithAccessToken

    def Post_Message(self, channel = None, text = None, username = None, attachments = None):
        if attachments is not None:
            if "__dict__" in dir(attachments):
                attachments = vars(attachments)

        if username and attachments is not None:
            slack_message = {
                "attachments": [attachments],
                "username": username
            }

            if (self.Send_to_Slack(slack_message)):
                return True
            else:
                return False
        elif channel and text and username and attachments is not None:
            slack_message = {
                "channel": channel,
                "text": text,
                "username": username,
                "attachments": [attachments]
            }

            if (self.Send_to_Slack(slack_message)):
                return True
            else:
                return False
        elif text and username is not None:
            slack_message = {
                "text": text,
                "username": username
            }

            if (self.Send_to_Slack(slack_message)):
                return True
            else:
                return False
        elif channel and text and username is not None:
            slack_message = {
                "text": text,
                "username": username,
                "channel": channel
            }

            if (self.Send_to_Slack(slack_message)):
                return True
            else:
                return False
        elif text is not None:
            slack_message = {
                "text": text
            }

            if (self.Send_to_Slack(slack_message)):
                return True
            else:
                return False

    def Send_to_Slack(self, payload):
        try:
            request = requests.post(
                url=self._uri,
                json=payload
            )

            if request.status_code is 200:
                return True
            else:
                return False
        except Exception:
            return False

class Field:
    def __init__(
        self, title = "", value = "", short = False
    ):
        self.Title = title
        self.Value = value
        self.Short = short

class Attachment:
    def __init__(
        self,
        color = None,
        pretext = None,
        text = None,
        fallback = None,
        author_name = None,
        author_link = None,
        author_icon = None,
        title = None,
        title_link = None,
        fields = None,
        image_url = None,
        thumb_url = None,
        footer = None,
        footer_icon = None,
        ts = None
    ):
        if color is not None:
            self.color = color
        if pretext is not None:
            self.pretext = pretext
        if text is not None:
            self.text = text
        if fallback is not None:
            self.fallback = fallback
        if author_name is not None:
            self.authorName = author_name
        if author_link is not None:
            self.authorLink = author_link
        if author_icon is not None:
            self.authorIcon = author_icon
        if title is not None:
            self.title = title
        if title_link is not None:
            self.titleLink = title_link
        if fields is not None:
            self.fields = fields
        if image_url is not None:
            self.imageUrl = image_url
        if thumb_url is not None:
            self.thumbUrl = thumb_url
        if footer is not None:
            self.footer = footer
        if footer_icon is not None:
            self.footerIcon = footer_icon
        if ts is not None:
            self.ts = ts

class SlackColors:
    Red = "#FF0000"
    Amber = "#FFBF00"
    Orange = "#FF9900"
    Yellow = "#FFFF00"
    Green = "#00FF00"
    LightBlue = "#00FFFF"
    DarkBlue = "#0000FF"
    White = "#FFFFFF"
    Gray = "#CCCCCC"
    DarkGray = "#808080"
    Black = "#000000"
    Chartreuse = "#7FFF00"
    Purple = "#800080"
