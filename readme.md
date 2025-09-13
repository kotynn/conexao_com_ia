# 🎙️ Transcrição e Análise de Áudio com AssemblyAI + Gemini + Kanban  

Este projeto automatiza o fluxo de **transcrever um áudio**, **analisar o texto com IA** (Google Gemini) e **enviar o resultado para um backend Kanban**.  

---

## 🚀 Funcionalidades  

1. **Transcrição de áudio** com [AssemblyAI](https://www.assemblyai.com/).  
2. **Análise semântica do texto** usando [Google Gemini](https://ai.google/).  
   - Retorna um JSON estruturado com:
     - `titulo`
     - `descricao`
     - `status` (`criado`, `atendido`, `fechado`)  
3. **Integração com Kanban** via API Flask (endpoint `/chamado/create`).  

---

## 📂 Estrutura do Projeto  

.
├── main.py # Código principal
├── requirements.txt # Dependências do projeto
└── README.md # Documentação


---

## ⚙️ Pré-requisitos  

- Python **3.9+**  
- Conta e **chave da API AssemblyAI**  
- Conta e **chave da API Google Gemini**  
- Backend Kanban rodando com endpoint `/chamado/create`  

---

## 📦 Instalação  

1. Clone o repositório:  
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo

    Crie um ambiente virtual (opcional, mas recomendado):

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

Instale as dependências:

    pip install -r requirements.txt

🔑 Configuração

No arquivo main.py, configure suas chaves de API e o endpoint do Kanban:

ASSEMBLY_KEY = "SUA_CHAVE_ASSEMBLYAI"
GEMINI_KEY = "SUA_CHAVE_GEMINI"
KANBAN_URL = "http://SEU_SERVIDOR:5000/chamado/create"

▶️ Como Usar

    Coloque seu arquivo de áudio em formato .mp3 ou .wav.

    No main.py, altere o caminho:

caminho_audio = "/caminho/do/seu/arquivo.mp3"

    Execute o script:

python main.py

📜 Exemplo de Saída
Entrada (áudio transcrito):

"Minha internet está fora do ar desde ontem."

Saída esperada do Gemini (JSON):

{
  "titulo": "Problema de internet",
  "descricao": "Usuário relata que está sem conexão de internet desde ontem.",
  "status": "criado"
}

⚠️ Tratamento de Erros

    ❌ Erro de transcrição → Problemas ao enviar áudio para AssemblyAI.

    ❌ Erro no Gemini → Resposta inválida ou não-JSON.

    ❌ Erro no Kanban → Falha ao enviar o chamado para o backend.

Todos os erros são exibidos no console com traceback para debug.
🛠️ Tecnologias

    Python 3

AssemblyAI

– Transcrição de áudio

Google Gemini

– Análise de texto com IA

Flask Kanban API

    – Backend de chamados

📄 Licença

Este projeto é de uso pessoal/educacional. Ajuste conforme suas necessidades.
📦 requirements.txt

requests
assemblyai
google-genai