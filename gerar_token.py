import os
from google_auth_oauthlib.flow import InstalledAppFlow

# O escopo deve ser o mesmo
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    if not os.path.exists('client_secret.json'):
        print("ERRO: O arquivo 'client_secret.json' precisa estar na pasta.")
        return

    # Deleta o token antigo para forçar uma geração limpa
    if os.path.exists('token.json'):
        os.remove('token.json')

    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    
    # --- MUDANÇA IMPORTANTE AQUI ---
    # access_type='offline': Pede o Refresh Token (eterno)
    # prompt='consent': Força a tela de permissão para garantir que o token venha completo
    creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')

    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    
    print("\nSUCESSO ABSOLUTO!")
    print("Verifique se dentro do arquivo 'token.json' existe a palavra 'refresh_token'.")
    print("Se existir, e seu app estiver publicado no Google Cloud, esse token não expira nunca.")

if __name__ == '__main__':
    main()