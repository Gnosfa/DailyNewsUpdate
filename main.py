def upload_to_google_drive(content):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    file_name = f"Daily_Update_{current_date}.md"
    
    FOLDER_ID = "1E7xTcbHuuWtxAOalgKzHby9bdj4ITAR-"
    
    file_metadata = {
        'name': file_name,
        'mimeType': 'text/markdown',
        'parents': [FOLDER_ID]
    }
    
    media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/markdown')
    
    # ✅ THIS BLOCK WAS MISSING — uploads the file first
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    ).execute()
    
    file_id = uploaded_file.get('id')
    
    # ✅ Then share it with your personal account
    service.permissions().create(
        fileId=file_id,
        body={
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'gnosfa@gmail.com'
        },
        supportsAllDrives=True
    ).execute()
    
    print(f"✅ File '{file_name}' uploaded. ID: {file_id}")
