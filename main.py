import os
import io
import time
import socket
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Safe timeout for your connection
socket.setdefaulttimeout(60)

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def download_folder_contents(folder_id, local_dir):
    service = get_service()
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    print("--- Fetching file list from Drive... ---")
    all_items = []
    page_token = None
    while True:
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=1000, fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token).execute()
        all_items.extend(results.get('files', []))
        page_token = results.get('nextPageToken')
        if not page_token: break

    # Filter out folders/docs to get true image count
    image_items = [i for i in all_items if 'google-apps' not in i['mimeType']]
    total = len(image_items)
    
    # Calculate current progress
    existing_files = [f for f in os.listdir(local_dir) if os.path.isfile(os.path.join(local_dir, f))]
    already_done = len(existing_files)
    
    print(f"\n{'='*40}")
    print(f"📊 PROGRESS: {already_done} / {total} images collected.")
    print(f"Remaining: {total - already_done} images.")
    print(f"{'='*40}\n")

    failed_files = []

    for index, item in enumerate(image_items, start=1):
        file_id = item['id']
        file_name = item['name']
        file_path = os.path.join(local_dir, file_name)

        if os.path.exists(file_path):
            # Just skip silently to keep the log clean for the new ones
            continue

        retries = 3
        for attempt in range(retries):
            fh = None
            try:
                request = service.files().get_media(fileId=file_id)
                fh = io.FileIO(file_path, 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    _, done = downloader.next_chunk()
                print(f"[{index}/{total}] ✅ Success: {file_name}")
                break 
            except Exception as e:
                if fh: fh.close()
                if attempt < retries - 1:
                    print(f"[{index}/{total}] ⚠️  Glitch on {file_name}, retrying... (Attempt {attempt+1})")
                    time.sleep(3)
                else:
                    print(f"[{index}/{total}] ❌ Failed: {file_name}")
                    failed_files.append(file_name)
            finally:
                if fh and not fh.closed:
                    fh.close()

    if failed_files:
        print(f"\n❌ Done with {len(failed_files)} errors. Run again to retry them.")

if __name__ == '__main__':
    TARGET_FOLDER_ID = '16Kgbyx_w0u2j-wwwRAxpCqsC0D2pENMB' 
    OUTPUT_DIRECTORY = 'MainaBiya'
    download_folder_contents(TARGET_FOLDER_ID, OUTPUT_DIRECTORY)