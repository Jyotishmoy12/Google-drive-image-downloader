# Google Drive Resumable Downloader

A robust, **"reliability-first"** Python script designed to download large batches of files (1,000+) from Google Drive. It was specifically built to handle unstable network connections and prevent the common **"browser crash"** or **"incomplete zip"** issues found in the Google Drive web interface.

---

## 🚀 Why This Exists

Downloading over 1,000 high-res images (like the MainaBiya project) is surprisingly difficult. Browsers often hang, and official **"Download as Zip"** links frequently fail or time out.

This script solves that by:

- **Resuming Naturally**  
  If your Wi-Fi drops, just run it again. It skips already-downloaded files automatically.

- **Handling SSL Errors**  
  Built-in retries for `[SSL: WRONG_VERSION_NUMBER]` glitches.

- **Sequential Stability**  
  One-by-one downloading ensures your laptop and network aren't overwhelmed.

---

## 🛠️ Setup

### 1️⃣ Enable Google Drive API

- Go to **Google Cloud Console**
- Enable the **Drive API**
- Download your `credentials.json`

### 2️⃣ Install Requirements

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
````

### 3️⃣ Configure

* Place `credentials.json` in the project folder.
* Update `TARGET_FOLDER_ID` in `main.py` with your Drive folder ID.

---

## 📈 Dashboard Features

Every time you run the script, it provides a real-time status update:

```
========================================
📊 PROGRESS: 193 / 1024 images collected.
Remaining: 831 images.
========================================
```

---

## 📝 Lessons Learned

### ⚖️ I/O vs. Speed

On fluctuating connections (tested in Guwahati, India), sequential downloading with a **60s timeout** outperformed multi-threading, which often led to SSL handshake failures.

### 📄 API Pagination

The script implements `nextPageToken` to ensure it sees beyond the standard 1,000-file API limit.

```
```
