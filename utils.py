from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import mimetypes
import logging
import os

TOKEN_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def authenticate_drive():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    return build('drive', 'v3', credentials=creds)


def upload_to_drive(file_path, unique_filename, id_pasta_drive):
    try:
        drive_service = authenticate_drive()
        
        # Descobre o tipo do arquivo (imagem/jpeg, video/mp4, etc)
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        # Metadados para o Drive
        file_metadata = {
            'name': unique_filename,
            'parents': [id_pasta_drive]
        }
        
        with open(file_path, 'rb') as f:
            # Usamos MediaIoBaseUpload em vez de MediaFileUpload
            media = MediaIoBaseUpload(f, mimetype=mime_type, resumable=True)
            
            # O upload acontece enquanto o arquivo está aberto
            drive_service.files().create(
                body=file_metadata, 
                media_body=media, 
                fields='id'
            ).execute()
        
        os.remove(file_path)
    
        logging.info(f"Arquivo '{unique_filename}' enviado para o Google Drive com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro no arquivo '{unique_filename}': {e}")
        