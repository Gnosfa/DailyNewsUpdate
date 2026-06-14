def upload_to_google_drive(content):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    file_name = f"Daily_Update_{current_date}.md"
    
    # ✅ Set this to your Google Drive folder ID
    FOLDER_ID = "1E7xTcbHuuWtxAOalgKzHby9bdj4ITAR-"  # <-- paste your folder ID
    
    file_metadata = {
        'name': file_name,
        'mimeType': 'text/markdown',
        'parents': [FOLDER_ID]  # ✅ Upload into your folder
    }
    
    media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/markdown')
    
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True  # ✅ Required for shared drives
    ).execute()
    
    print(f"✅ File '{file_name}' uploaded successfully. ID: {uploaded_file.get('id')}")