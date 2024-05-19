import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError
from requests.exceptions import HTTPError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

try:
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
except RefreshError as e:
    print(f"Error refreshing credentials: {e}")

service = build('gmail', 'v1', credentials=creds)
message = MIMEText('Już o 16.20 odbywa się twój lot. Upewnij się, że masz ze sobą wszsytkie potrzebne rzeczy i sprawdź stan swojego bagażu')
message['To'] = 'examplemail@gmail.com'
message['Subject'] = 'Email Subject'
create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

try:
    sent_message = service.users().messages().send(userId="me", body=create_message).execute()
    print(f'Sent message with ID: {sent_message["id"]}')
except HTTPError as error:
    print(f'An error occurred: {error}')