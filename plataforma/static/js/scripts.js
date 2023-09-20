function toggleFullScreen(videoId) {
    const video = document.getElementById(videoId);

    if (!document.fullscreenElement) {
        video.requestFullscreen().catch(err => {
            alert(`Erro ao entrar em tela cheia: ${err.message}`);
        });
    } else {
        document.exitFullscreen();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const categoryFilter = document.getElementById("category-filter");
    const fileCategories = document.querySelectorAll(".file-category");

    categoryFilter.addEventListener("change", function () {
        const selectedCategory = categoryFilter.value;

        fileCategories.forEach(function (category) {
            if (selectedCategory === "all" || category.classList.contains(selectedCategory)) {
                category.style.display = "block";
            } else {
                category.style.display = "none";
            }
        });
    });
});
function verificarDados() {
    // Simule a verificação dos dados (substitua esta parte pelo seu código de verificação)
    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const telefone = document.getElementById("telefone").value;

    // Verifique os dados no servidor (substitua esta parte pelo seu código de verificação)
    // Suponha que o servidor retorne um objeto JSON com a resposta
    fetch('/verificar_dados_usuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nome: nome,
            email: email,
            telefone: telefone
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.valid) {
            document.getElementById("dados-validos-message").textContent = "Dados válidos.";
            document.getElementById("dados-invalidos-message").textContent = "";
            document.getElementById("redefinir-senha").style.display = "block";
        } else {
            document.getElementById("dados-validos-message").textContent = "";
            document.getElementById("dados-invalidos-message").textContent = "Dados inválidos.";
            document.getElementById("redefinir-senha").style.display = "none";
        }
    })
    .catch(error => console.error('Erro:', error));
}

function redefinirSenha() {
    const novaSenha = document.getElementById("nova-senha").value;
    const nome = document.getElementById("nome").value; // Adicione esta linha para obter o nome

    // Redefina a senha no servidor (substitua esta parte pelo seu código de redefinição)
    // Suponha que o servidor retorne um objeto JSON com a resposta
    fetch('/redefinir_senha', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            novaSenha: novaSenha,
            nome: nome // Adicione o campo 'nome' aqui para identificar o usuário
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("senha-redefinida-message").textContent = "Senha redefinida com sucesso!";
            document.getElementById("senha-nao-redefinida-message").textContent = "";
        } else {
            document.getElementById("senha-redefinida-message").textContent = "";
            document.getElementById("senha-nao-redefinida-message").textContent = "Não foi possível redefinir a senha.";
        }
    })
    .catch(error => console.error('Erro:', error));
}





document.addEventListener('DOMContentLoaded', function () {
    const categoryLinks = document.querySelectorAll('#category-filter a');

    categoryLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();

            const targetId = link.getAttribute('href').substring(1); // Remove o caractere '#' do href
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                const offset = 85; // Define o deslocamento desejado
                const targetPosition = targetElement.offsetTop - offset;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth' // Rola suavemente para a posição
                });
            }
        });
    });
});