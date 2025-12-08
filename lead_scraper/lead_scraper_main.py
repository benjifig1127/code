from datetime import datetime, timedelta
from time import sleep
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
QUERY = 'is:unread subject:"test2"'
NEEDLE = "<https://schedule.planhero.com/events/"
TIMEOUT = 300
SLEEP = 1

def auth():
  try:
    return Credentials.from_authorized_user_file("token.json", SCOPES)
  except:
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    with open("token.json", "w") as token_file:
      token_file.write(credentials.to_json())
    return credentials

def extract_url(messages, service):
  msg_id = messages[0]["id"]
  messages_extracted = service.users().messages().get(userId="me", id=msg_id, format="full").execute()

  payload_parts = messages_extracted["payload"].get("parts", [])
  for payload in payload_parts:
    mimmeType = payload["mimeType"]
    if mimmeType != "text/plain":
      continue
    body = payload["body"]["data"]
    text_body = base64.urlsafe_b64decode(body).decode().split("\n")
    for line in text_body:
      if NEEDLE not in line:
        continue
      return line.replace(">", "").replace("<", "").strip()
  raise Exception("no url found, contact ben")

def main():
  timeout = datetime.now() + timedelta(seconds=TIMEOUT)
  print("setting timeout at " + timeout.strftime("%H:%M:%S"))

  service = build("gmail", "v1", credentials=auth())
  while datetime.now() <= timeout:
    query_result = service.users().messages().list(userId="me", q=QUERY).execute()

    msgs = query_result.get("messages", [])
    if not msgs:
      print("sleping while waiting for email...")
      sleep(SLEEP)
      continue

    url = extract_url(msgs, service)
    print(url)
    return

if __name__ == "__main__":
  main()            