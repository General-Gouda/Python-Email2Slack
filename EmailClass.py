from datetime import datetime, tzinfo, timezone

class EmailObject:
    def __init__(self, body_preview, email_subject, email_sent_datetime, email_body_html, email_sent_from, email_id):
        self.Body_Preview = body_preview
        self.Email_Subject = email_subject

        dt = datetime.strptime(email_sent_datetime, '%Y-%m-%dT%H:%M:%Sz')
        dt = dt.replace(tzinfo=timezone.utc)
        dt = dt.astimezone()

        self.Email_Sent_DateTime = dt
        self.Email_Body_Html = email_body_html
        self.Email_Sent_From = email_sent_from
        self.Email_ID = email_id