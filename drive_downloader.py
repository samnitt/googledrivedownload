import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Authenticate and create the service
def authenticate_drive_api():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

# Load downloaded files log (text format)
def load_downloaded_log():
    if os.path.exists('download_log.txt'):
        with open('download_log.txt', 'r') as f:
            return set(line.strip() for line in f.readlines())
    else:
        return set()

# Save new file ID to log
def append_to_log(file_id):
    with open('download_log.txt', 'a') as f:
        f.write(file_id + '\n')

# Create folder if doesn't exist
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Download a single file
def download_file(service, file_id, file_name, mime_type, parent_path):
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)

    # Handle export for Google Docs, Sheets, Slides
    if mime_type == "application/vnd.google-apps.document":
        export_ext = "docx"
        request = service.files().export_media(
            fileId=file_id,
            mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    elif mime_type == "application/vnd.google-apps.spreadsheet":
        export_ext = "xlsx"
        request = service.files().export_media(
            fileId=file_id,
            mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    elif mime_type == "application/vnd.google-apps.presentation":
        export_ext = "pptx"
        request = service.files().export_media(
            fileId=file_id,
            mimeType="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    else:
        export_ext = None
        request = service.files().get_media(fileId=file_id)

    # Correct file name
    if export_ext:
        file_base = os.path.splitext(file_name)[0]
        file_name = f"{file_base}.{export_ext}"

    file_path = os.path.join(parent_path, file_name)

    # Actual download
    fh = io.FileIO(file_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Downloading {file_name}: {int(status.progress() * 100)}%.")
    print(f"✅ Download completed: {file_name}")
    return True  # Success

# Recursive function to download all folders and files
def traverse_and_download(service, folder_id, parent_path, downloaded_log):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    for item in items:
        file_id = item['id']
        file_name = item['name']
        mime_type = item['mimeType']

        if mime_type == 'application/vnd.google-apps.folder':
            # It's a folder
            new_folder_path = os.path.join(parent_path, file_name)
            create_folder(new_folder_path)
            traverse_and_download(service, file_id, new_folder_path, downloaded_log)
        else:
            # It's a file
            if file_id not in downloaded_log:
                try:
                    success = download_file(service, file_id, file_name, mime_type, parent_path)
                    if success:
                        append_to_log(file_id)  # Save only after successful download
                        downloaded_log.add(file_id)  # Update in-memory too
                except Exception as e:
                    print(f"⚠️ Error downloading {file_name}: {e}")
            else:
                print(f"⏩ Skipping already downloaded file: {file_name}")

# Main Function
def download_files_from_drive():
    service = authenticate_drive_api()
    downloaded_log = load_downloaded_log()

    # Define your Google Drive root folder ID
    drive_root_folder_id = 'root'

    base_folder = 'Downloaded_Drive'
    create_folder(base_folder)

    traverse_and_download(service, drive_root_folder_id, base_folder, downloaded_log)

if __name__ == '__main__':
    download_files_from_drive()
