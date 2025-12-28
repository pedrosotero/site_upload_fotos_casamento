import os
from flask import Flask, render_template, request, redirect, url_for
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from werkzeug.utils import secure_filename
import mimetypes
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# Configurações
UPLOAD_FOLDER = 'tmp' # Em produção (Render/Heroku), use /tmp
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json' 
TOKEN_FILE = 'token.json'
PARENT_FOLDER_ID = '11Q_spbIp1YbffRLsFapiAfDfFnGSBfPi'
ID_PASTA_IGREJA = '1-sJV6ANRh2_nx-7FkR5winl0i4lbTn5v'
ID_PASTA_RECEPCAO = '1a0mfkNXzrvvEJcqGVtukNUzvnZ5RaY5y'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def authenticate_drive():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    return build('drive', 'v3', credentials=creds)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', senha_incorreta=False)
        
    if request.method == 'POST':
        if request.form.get('senha', '') != 'vivaosnoivos':
            return render_template('index.html', senha_incorreta=True)
            
        if 'files[]' not in request.files:
            return redirect(request.url)
        
        files = request.files.getlist('files[]')
        
        guest_name = request.form.get('guest_name', 'Sem Nome')
        local = request.form.get('location', 'Recepção')
        
        id_pasta_drive = ID_PASTA_IGREJA if local == 'Igreja' else ID_PASTA_RECEPCAO
        
        # Sanitiza o nome para evitar caracteres estranhos na criação da pasta
        safe_guest_name = "".join([c for c in guest_name if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')
        
        drive_service = authenticate_drive()
        
        for file in files:
            if file.filename == '' or not allowed_file(file.filename):
                continue # Pula arquivos suspeitos
            
            # Sanitiza nome e adiciona UUID para evitar sobrescrita
            original_filename = secure_filename(file.filename)
            extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
            unique_filename = f"{safe_guest_name}_{uuid.uuid4().hex[:8]}.{extension}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            # Salva temporariamente no servidor
            file.save(file_path)
            
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
            
        return render_template('success.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)