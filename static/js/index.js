// 1. Lógica de Cookies/LocalStorage para o Nome
document.addEventListener('DOMContentLoaded', function () {
    const nameInput = document.getElementById('guest_name');
    const savedName = localStorage.getItem('wedding_guest_name');

    if (savedName) {
        nameInput.value = savedName;
    }

    nameInput.addEventListener('input', function () {
        localStorage.setItem('wedding_guest_name', this.value);
    });
});

// 2. Feedback visual de quantos arquivos foram escolhidos
const MAX_FILE_SIZE = 25 * 1024 * 1024;

function updateFileName(input) {
    const feedback = document.getElementById('file-feedback');
    const submitBtn = document.querySelector('.btn-submit'); // Pega o botão de enviar

    if (input.files && input.files.length > 0) {
        let totalFiles = input.files.length;
        let invalidFiles = [];

        // Verifica cada arquivo individualmente
        for (let i = 0; i < totalFiles; i++) {
            if (input.files[i].size > MAX_FILE_SIZE) {
                invalidFiles.push(input.files[i].name);
            }
        }

        if (invalidFiles.length > 0) {
            // Se tiver arquivo grande demais
            feedback.innerHTML = `
                <span class="text-danger fw-bold">
                    <i class="fas fa-exclamation-triangle"></i> 
                    Arquivo muito grande (Máx 25MB):<br>
                    ${invalidFiles.join(', ')}
                </span>`;

            // Desabilita o botão de enviar para evitar erro no servidor
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.5';
            input.value = ""; // Opcional: Limpa a seleção
        } else {
            // Tudo certo
            feedback.textContent = `${totalFiles} arquivo(s) selecionado(s)`;
            feedback.style.color = '#D4AF37';
            feedback.style.fontWeight = 'bold';

            // Reabilita o botão
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
        }
    } else {
        feedback.textContent = 'Nenhum arquivo selecionado';
        feedback.style.color = '#aaa';
        feedback.style.fontWeight = 'normal';
        submitBtn.disabled = false;
    }
}

// 3. Mostrar overlay de Loading ao enviar
document.getElementById('uploadForm').addEventListener('submit', function (e) {
    const files = document.getElementById('files').files;
    if (files.length === 0) {
        e.preventDefault();
        alert('Por favor, selecione pelo menos uma foto!');
        return;
    }
    // Mostra o loading
    document.getElementById('loadingOverlay').style.display = 'flex';
});

// Lógica do Olho Mágico (Ver/Ocultar Senha)
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('senha');

togglePassword.addEventListener('click', function () {
    // Alterna o tipo do input
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    // Alterna o ícone (olho aberto / fechado)
    const icon = this.querySelector('i');
    icon.classList.toggle('fa-eye');
    icon.classList.toggle('fa-eye-slash');
});