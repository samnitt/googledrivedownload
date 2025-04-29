# 📁 Google Drive Folder & File Downloader

This Python script recursively downloads all files and folders from your **Google Drive** to a local directory. It supports conversion of Google Docs, Sheets, and Slides into Microsoft Office-compatible formats and avoids duplicate downloads by maintaining a log of already downloaded file IDs.

---

## ✅ Features

- 🔐 Authenticates with Google Drive via OAuth 2.0
- 📁 Recursively downloads all files and folders
- 🔄 Converts:
  - Google Docs → `.docx`
  - Google Sheets → `.xlsx`
  - Google Slides → `.pptx`
- 📜 Maintains a log (`download_log.txt`) to skip files already downloaded

---

## 🛠️ Setup Instructions

### 1. 📂 Clone the Repository

```
bash
git clone https://github.com/your-username/google-drive-downloader.git
cd google-drive-downloader
```

### 2. 🐍 Create Virtual Environment (Optional but Recommended)

```
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. 📦 Install Dependencies

```
pip install -r requirements.txt
```

### 🔐 Enable Google Drive API & Get Credentials

Go to the Google Cloud Console.

Create a new project (or use an existing one).

Go to APIs & Services > Library.

Search for Google Drive API and click Enable.

Then go to APIs & Services > Credentials.

Click Create Credentials > OAuth client ID:

Choose Desktop App as the application type.

Give it a name like DriveDownloader.

Click Download JSON and save the file as credentials.json in the same directory as your script.

✅ On first run, the script will open a browser window asking you to log in and authorize access. After that, it stores your credentials in token.pickle.

### 🚀 Usage

```
python drive_downloader.py
```

Output
All downloaded files will be saved in the Downloaded_Drive/ folder.

A download_log.txt file will track downloaded file IDs to avoid re-downloading.

File conversion will happen automatically for Google Docs/Sheets/Slides.

### 🔄 Download From a Specific Folder

By default, the script downloads from your root folder. To download from a specific folder:

Open the folder in Google Drive.

Copy the folder ID from the URL. For example:

https://drive.google.com/drive/folders/1aBcDeFGhiJKlmnOpQRs

Edit the script:

drive_root_folder_id = '1aBcDeFGhiJKlmnOpQRs'  # Replace with your folder ID

### 🗃️ Project Structure

```
.
├── drive_downloader.py       # Your main script
├── credentials.json          # Downloaded from Google Cloud Console
├── token.pickle              # Auto-created after first auth
├── download_log.txt          # Auto-created log of downloaded file IDs
├── Downloaded_Drive/         # Folder where files are saved
├── README.md                 # You're reading this
└── requirements.txt          # Required packages
```

### ⚠️ Notes

The app uses read-only access to your Google Drive.

Ensure credentials.json is kept private and not committed to public repositories.

Files already in download_log.txt will not be downloaded again.

Folder structures will be recreated locally.

### 📄 License

This project is licensed under the MIT License.

### 🙋‍♂️ Questions?

Feel free to raise an issue or contact the author for support.


