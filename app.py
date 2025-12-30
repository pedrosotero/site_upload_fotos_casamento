from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from utils import allowed_file, upload_to_drive
import threading
import logging
import uuid
import os

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

# Configurações
UPLOAD_FOLDER = 'tmp' # Em produção (Render/Heroku), use /tmp
SERVICE_ACCOUNT_FILE = 'credentials.json' 
PARENT_FOLDER_ID = '11Q_spbIp1YbffRLsFapiAfDfFnGSBfPi'
ID_PASTA_IGREJA = '1-sJV6ANRh2_nx-7FkR5winl0i4lbTn5v'
ID_PASTA_RECEPCAO = '1a0mfkNXzrvvEJcqGVtukNUzvnZ5RaY5y'


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


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
        
        qtd_fotos = 0
        for file in files:
            if file.filename == '' or not allowed_file(file.filename):
                continue # Pula arquivos suspeitos
            
            # Sanitiza nome e adiciona UUID para evitar sobrescrita
            original_filename = secure_filename(file.filename)
            extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
            unique_filename = f"{safe_guest_name}_{uuid.uuid4().hex}.{extension}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            # Salva temporariamente no servidor
            file.save(file_path)
            
            thread = threading.Thread(target=upload_to_drive, args=(file_path, unique_filename, id_pasta_drive))
            thread.start()
            
            qtd_fotos += 1
            
        return render_template('success.html', qtd_fotos=qtd_fotos)

    return render_template('index.html')


@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('error_413.html'), 413


if __name__ == '__main__':
    app.run(debug=False)