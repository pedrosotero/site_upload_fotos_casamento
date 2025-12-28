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
function updateFileName(input) {
    const feedback = document.getElementById('file-feedback');
    if (input.files && input.files.length > 0) {
        feedback.textContent = `${input.files.length} arquivo(s) selecionado(s)`;
        feedback.style.color = '#D4AF37';
        feedback.style.fontWeight = 'bold';
    } else {
        feedback.textContent = 'Nenhum arquivo selecionado';
        feedback.style.color = '#aaa';
        feedback.style.fontWeight = 'normal';
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