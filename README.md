# 📊 Fornecedor Insight

Sistema em Flask que consulta dados de empresas via API pública (BrasilAPI), calcula nível de risco e armazena histórico em JSON. (O sistema está em com deploy no Render, mas por algumas limitações do mesmo algumas funções podem falharem, é recomendado caso aconteça, clonar na máquina pessoal.) 

---

# 🎯 Desafio Técnico

Desenvolver um sistema que colete informações de uma API pública ou site e exiba em tabela.

## 📌 Dados esperados:
- Data
- Título / Assunto
- Resumo
- Link
- Fonte

---

## 📌 Requisitos do desafio

- Coleta via API pública ou scraping simples
- Armazenamento simples (JSON ou memória)
- Backend em Python (Flask)
- Interface HTML com tabela e busca

---

# ⚙️ Pré-requisitos

Antes de começar, você precisa ter instalado:

### ✔ Python
- Versão 3.10 ou superior  
- Download: https://www.python.org/downloads/

Para verificar:
```bash
python --version
```

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/FernandaGabrielli/fornecedor-insight.git
cd fornecedor-insight
```

### 2. Criar ambiente virtual (recomendado)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## ▶️ Executar o projeto

```bash
python app.py
```

ou

```bash
python3 app.py
```

---

## 🌐 Acessar no navegador

```
http://127.0.0.1:5000
```

---

## 🧠 Como o sistema funciona

1. Usuário digita um CNPJ
2. Sistema consulta a BrasilAPI
3. Retorna dados da empresa
4. Calcula nível de risco automaticamente
5. Salva consulta no histórico (`historico.json`)
6. Exibe histórico em tabela na interface

---

## 📊 Funcionalidades

- Consulta de CNPJ via API
- Exporta via EXCEL
- Cálculo automático de risco
- Histórico persistente em JSON
- Interface web simples
- Exibição em tabela

---

## 📌 Exemplo de uso

```
CNPJ: 00.623.904/0001-73
→ Empresa encontrada
→ Risco: BAIXO
→ Registro salvo no histórico
```

---

## ⚠️ Observações importantes

- Projeto **não** usa banco de dados
- Dados são salvos em JSON local
- Depende da BrasilAPI estar online
- Requer internet para consultas

---
