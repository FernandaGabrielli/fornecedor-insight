// ===============================
// ELEMENTOS DA INTERFACE
// ===============================

// Campo de busca textual
const searchInput = document.getElementById("searchInput");

// Campo de filtro de risco
const riskFilter = document.getElementById("riskFilter");

// Todas as linhas do histórico
function getRows() {
    return document.querySelectorAll("#historyTable tbody tr");
}


// ===============================
// FUNÇÃO DE FILTRO DA TABELA
// ===============================

function filtrarTabela() {

    const search = searchInput.value.toLowerCase();

    const risk = riskFilter.value.toLowerCase();

    rows.forEach(row => {

        // EMPRESA = coluna 2
        const empresa = row.children[2]
            .innerText
            .toLowerCase();

        // CNPJ = coluna 3
        const cnpj = row.children[3]
            .innerText
            .toLowerCase();

        // RESUMO = coluna 4
        const resumo = row.children[4]
            .innerText
            .toLowerCase();

        // risco vindo do backend
        const risco = (row.dataset.risk || "").toLowerCase();

        const correspondeBusca = (
            empresa.includes(search)
            || cnpj.includes(search)
            || resumo.includes(search)
        );

        const correspondeRisco = (
            risk === ""
            || risco.includes(risk)
        );

        row.style.display = (
            correspondeBusca
            && correspondeRisco
        )
            ? ""
            : "none";

    });

}

// ===============================
// EVENTOS
// ===============================

// Busca dinâmica ao digitar
searchInput.addEventListener(
    "keyup",
    filtrarTabela
);

// Filtro dinâmico ao trocar risco
riskFilter.addEventListener(
    "change",
    filtrarTabela
);


// ===============================
// LINHA CLICÁVEL DO HISTÓRICO
// ===============================

document.querySelector("#historyTable tbody")
    .addEventListener("click", (e) => {

        const row = e.target.closest("tr");

        if (!row) return;

        const cnpj = row.dataset.cnpj;

        document.querySelector('input[name="cnpj"]').value = cnpj;
        document.querySelector('input[name="cnpj"]').form.submit();
    });

// ===============================
// SCROLL AUTOMÁTICO PARA RESULTADO
// ===============================

window.addEventListener("load", () => {

    // Card de resultado
    const resultado = document.getElementById(
        "empresaResultado"
    );

    // Se existir resultado, sobe automaticamente
    if (resultado) {

        resultado.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }

});

    // =========================
// ABRIR EMPRESA PELO CARD
// =========================

function abrirHistorico(cnpj) {

    // Remove tudo que não for número
    const cnpjLimpo = cnpj.replace(/\D/g, "");

    // Campo hidden
    document
        .getElementById("historyCnpj")
        .value = cnpjLimpo;

    // Envia formulário
    document
        .getElementById("historyForm")
        .submit();

}
// ===============================
// EXPORTAR SELECIONADOS
// ===============================

function exportarSelecionados() {

    // Todos os checkboxes marcados
    const selecionados = document.querySelectorAll(
        ".history-checkbox:checked"
    );

    // Se NÃO selecionar nenhum → exporta tudo
    if (selecionados.length === 0) {

        window.location.href = "/exportar-historico";

        return;

    }

    // Pega os índices selecionados
    const indices = [];

    selecionados.forEach(item => {

        indices.push(item.value);

    });

    // Monta URL
    const query = indices.join(",");

    // Redireciona
    window.location.href =
        `/exportar-historico?indices=${query}`;

}


// ===============================
// CHECKBOX MARCAR TODOS
// ===============================

const checkAll = document.getElementById("checkAll");

if (checkAll) {

    checkAll.addEventListener("change", function () {

        const checkboxes = document.querySelectorAll(
            ".history-checkbox"
        );

        checkboxes.forEach(cb => {

            cb.checked = this.checked;

        });

    });

}

// ===============================
// BOTÃO APAGAR
// ===============================

const deleteBtn = document.getElementById(
    "deleteBtn"
);

// Atualiza visibilidade do botão
function atualizarBotaoApagar() {

    if (!deleteBtn) return;

    const selecionados = document.querySelectorAll(
        ".history-checkbox:checked"
    );

    if (selecionados.length > 0) {
        deleteBtn.classList.remove("d-none");
    } else {
        deleteBtn.classList.add("d-none");
    }
}


// Escuta mudança nos checkboxes
document.querySelectorAll(
    ".history-checkbox"
).forEach(checkbox => {

    checkbox.addEventListener(
        "change",
        atualizarBotaoApagar
    );

});


// ===============================
// APAGAR REGISTROS
// ===============================

function apagarSelecionados() {

    const selecionados = document.querySelectorAll(
        ".history-checkbox:checked"
    );

    // Nenhum selecionado
    if (selecionados.length === 0) {

        return;

    }

    // Confirmação
    const confirmar = confirm(
        "Deseja realmente apagar os registros selecionados?"
    );

    // Cancelou
    if (!confirmar) {

        return;

    }

    // Pega índices
    const indices = [];

    selecionados.forEach(item => {

        indices.push(item.value);

    });

    // Envia para backend
    fetch("/apagar-historico", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ indices })
    })
    .then(res => {
        if (!res.ok) throw new Error("Erro ao apagar");
        return res.json();
    })
    .then(() => location.reload())
    .catch(err => alert(err.message));

    }

// ===============================
// BOTÃO CONSULTAR / FECHAR DINÂMICO
// ===============================

// Campo CNPJ
const cnpjInput = document.querySelector(
    'input[name="cnpj"]'
);

// Botão principal
const consultarBtn = document.getElementById(
    "consultarBtn"
);

// Resultado aberto
const empresaResultado = document.getElementById(
    "empresaResultado"
);

// Função para resetar interface
function resetarConsulta() {

    // Se não existir resultado aberto, ignora
    if (!empresaResultado) {

        return;

    }

    // Remove card resultado
    empresaResultado.remove();

    // Remove card de sócios
    const sociosCard = document.querySelectorAll(
        ".shadow-custom.mt-4.p-4"
    );

    sociosCard.forEach(card => {

        // evita apagar histórico
        if (
            !card.id ||
            card.id !== "historySection"
        ) {

            // se tiver tabela de sócios
            if (
                card.innerText.includes("Sócios")
            ) {

                card.remove();

            }

        }

    });

    // Volta botão para CONSULTAR
    consultarBtn.innerText = "Consultar";

    consultarBtn.classList.remove(
        "btn-outline-secondary"
    );

    consultarBtn.classList.add(
        "btn-primary"
    );

}
if (consultarBtn) {

    consultarBtn.addEventListener("click", (e) => {

        const empresaResultado = document.getElementById("empresaResultado");

        if (!empresaResultado) return;

        e.preventDefault();

        empresaResultado.remove();

        consultarBtn.innerText = "Consultar";
        consultarBtn.classList.remove("btn-outline-secondary");
        consultarBtn.classList.add("btn-primary");
    });
}
// ===============================
// DIGITOU NOVO CNPJ
// ===============================

if (cnpjInput) {

    cnpjInput.addEventListener(
        "input",
        resetarConsulta
    );

}

// ===============================
// FILTRO DO HISTÓRICO

if (searchInput) {

    searchInput.addEventListener(
        "input",
        resetarConsulta
    );

}

if (riskFilter) {

    riskFilter.addEventListener(
        "change",
        resetarConsulta
    );

}