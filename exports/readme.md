🚜 Data Harvester 3.0 (Firefox Edition)

Data Harvester é uma ferramenta de engenharia de dados universal projetada para coletar, limpar e estruturar informações da web de forma automática. Diferente de scrapers simples, ele utiliza um motor híbrido (Requests para velocidade e Selenium/Firefox para sites dinâmicos) e processamento paralelo para alta performance.
✨ Funcionalidades Principais

    ⚡ Modo Turbo (Multithreading): Processa múltiplos sites simultaneamente, reduzindo drasticamente o tempo de coleta.

    🦊 Híbrido & Dinâmico: Alterna entre Requests (leve) e Selenium GeckoDriver (para sites com JavaScript, React, Angular).

    📊 Extração Inteligente: Identifica e estrutura automaticamente:

        Títulos (H1-H3)

        Parágrafos de conteúdo

        Links úteis

        Tabelas HTML (converte automaticamente para abas no Excel)

        Metadados (SEO descriptions, keywords)

    🛡️ Resiliência: Sistema de Retry automático para falhas de conexão e rotação de User-Agent para evitar bloqueios.

    📑 Saída Organizada: Gera arquivos JSON (dados brutos) e Excel (.xlsx) com abas separadas para cada tipo de dado.

    📝 Logs Profissionais: Rastreabilidade completa via arquivo execution.log.

🛠️ Instalação
Pré-requisitos

    Python 3.8+ instalado.

    Mozilla Firefox instalado na máquina (para o modo dinâmico).

Passo a Passo

    Clone o repositório:
    Bash

git clone https://github.com/gabiRioRange/data-harvester.git
cd data-harvester

Crie e ative um ambiente virtual (recomendado):
Bash

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

Instale as dependências:
Bash

    pip install requests beautifulsoup4 pandas lxml openpyxl selenium webdriver-manager fake-useragent

🚀 Como Usar

Execute o script principal:
Bash

python harvester.py

Você verá um menu interativo:
Opção 1: Teste Único

Ideal para testar uma URL específica rapidamente. O script perguntará a URL e salvará os dados.
Opção 2: Processamento em Lote (Turbo)

Lê um arquivo de texto com múltiplas URLs e processa todas em paralelo.

    Crie um arquivo chamado urls.txt na pasta do projeto.

    Adicione um link por linha:
    Plaintext

    https://www.python.org
    https://news.ycombinator.com
    https://exemplo.com/dados-financeiros

    Escolha a Opção 2 no menu.

    Defina se deseja usar o Firefox (Modo Dinâmico) ou Requests (Modo Rápido).

📂 Estrutura do Projeto
Plaintext

data-harvester/
│
├── exports/               # 📂 Onde os dados (JSON/Excel) são salvos automaticamente
│   ├── python_org_20231208.xlsx
│   └── python_org_20231208.json
│
├── harvester.py           # 🧠 O cérebro do scraper (Script Principal)
├── urls.txt               # 📄 Lista de sites para processamento em lote
├── execution.log          # 📝 Histórico de erros e sucessos
└── README.md              # 📄 Documentação

💾 Exemplo de Saída (Excel)

O arquivo Excel gerado é altamente organizado:
Aba	Conteúdo
Metadata	Título da página, URL, Data da coleta, Description.
Links	Lista de todos os links encontrados e seus textos.
Conteudo_Texto	Todos os cabeçalhos e parágrafos em ordem de leitura.
Tabela_0, Tabela_1...	Cada tabela HTML encontrada vira uma aba separada e limpa.
👤 Autor

Gabriel - Desenvolvedor Python | Backend & Automação