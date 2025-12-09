<h1 align="left">🚜 Data Harvester 3.0 (Firefox Edition)</h1>

###

<h3 align="left">Digital Craftsman Backend | Automação | Dados</h3>

###

<img align="right" height="150" src="https://i.imgflip.com/ae5t3z.gif" />

###

<p align="left">O <b>Data</b> Harvester é uma ferramenta robusta de <b>engenharia de dados universal</b> para coletar, limpar e estruturar informações da web. <br>Ele utiliza um <b>motor híbrido</b> (Requests para velocidade e Selenium/Firefox para dinâmica) e processamento paralelo para garantir alta performance e resiliência em qualquer tipo de site.</p>

###

<h3 align="left">Digital Craftsman Backend | Automação | Dados</h3>

[<img src="https://img.shields.io/static/v1?message=Status%3A%20Estável&logo=python&label=&color=009688&logoColor=white&labelColor=232323&style=for-the-badge" height="30" alt="" />](URL_DO_SEU_PROJETO)
<img src="https://img.shields.io/static/v1?message=Python%203.8%2B&logo=python&label=&color=3776AB&logoColor=white&labelColor=232323&style=for-the-badge" height="30" alt="Python 3.8+ Versão" />
[<img src="https://img.shields.io/static/v1?message=Licença%3A%20MIT&logo=github&label=&color=F05032&logoColor=white&labelColor=232323&style=for-the-badge" height="30" alt="" />](URL_DA_SUA_LICENCA)

###

---

###

<h2 align="left">✨ Funcionalidades Principais</h2>

###

<p align="left">O Data Harvester foi construído com foco em velocidade, resiliência e organização da saída de dados:</p>

###

<ul align="left">
    <li><strong>⚡ Modo Turbo (Multithreading):</strong> Processa múltiplos sites simultaneamente, reduzindo drasticamente o tempo de coleta em lote.</li>
    <li><strong>🦊 Híbrido & Dinâmico:</strong> Alterna entre <code>Requests</code> (leve) e <code>Selenium/GeckoDriver</code> (para sites com JavaScript, React, Angular).</li>
    <li><strong>📊 Extração Inteligente:</strong> Identifica e estrutura automaticamente Títulos, Parágrafos, Links e <b>Tabelas HTML</b> (conversão automática para Excel).</li>
    <li><strong>🛡️ Resiliência:</strong> Sistema de Retry automático para falhas de conexão e rotação de User-Agent.</li>
    <li><strong>📑 Saída Organizada:</strong> Gera arquivos <b>JSON</b> e <b>Excel (.xlsx)</b> com abas separadas para cada tipo de dado.</li>
</ul>

###

---

###

<h2 align="left">🛠️ Instalação (Python)</h2>

###

<h3 align="left">Pré-requisitos</h3>

<p align="left">O projeto requer apenas o <b>Python 3.8+</b> e o <b>Mozilla Firefox</b> (para o modo dinâmico) instalados.</p>

###

<h3 align="left">Passo a Passo</h3>

<p align="left"><strong>1. Clone o repositório:</strong></p>

bash

    git clone [https://github.com/gabiRioRange/data-harvester.git](https://github.com/gabiRioRange/data-harvester.git)
    cd data-harvester
    
<p align="left"><strong>2. Crie e ative um ambiente virtual (Recomendado):</strong></p>

     python -m venv .venv
# Windows:
    .venv\Scripts\activate
# Linux/Mac:
    source .venv/bin/activate

<p align="left"><strong>3. Instale as dependências:</strong></p>

    pip install requests beautifulsoup4 pandas lxml openpyxl selenium webdriver-manager fake-useragent

<h2 align="left">🚀 Como Usar</h2>

<p align="left">Execute o <code>harvester.py</code> e escolha a opção no menu interativo:</p>

    python harvester.py
    
<h4 align="left">Opção 1: Teste Único</h4>

<p align="left">Ideal para testar uma URL específica rapidamente. O script perguntará a URL e salvará os dados.</p>

<h4 align="left">Opção 2: Processamento em Lote (Turbo)</h4>

<p align="left">Permite ler o arquivo <code>urls.txt</code> (um link por linha) e processar todas as URLs em paralelo.</p>

<h2 align="left">📂 Estrutura do Projeto e Saída</h2>

<p align="left">O projeto é estruturado para facilitar a manutenção e a rastreabilidade (<code>execution.log</code>).</p>
Plaintext

data-harvester/

    │
    ├── exports/             # 📂 Onde os dados (JSON/Excel) são salvos automaticamente
    ├── harvester.py         # 🧠 O cérebro do scraper
    ├── urls.txt             # 📄 Lista de sites para processamento em lote
    └── execution.log        # 📝 Histórico de erros e sucessos

<p align="left">O arquivo Excel gerado possui abas separadas para <strong>Metadata</strong>, <strong>Links</strong>, <strong>Conteudo_Texto</strong> e abas numeradas para cada <strong>Tabela HTML</strong> encontrada.</p>

<h2 align="left">👤 Autor e Contato</h2>

<h4 align="left">Gabriel - Desenvolvedor Python | Backend & Automação</h4>

###

<div align="left">
  <a href="https://github.com/gabiRioRange">
    <img src="https://img.shields.io/static/v1?message=GitHub&logo=github&label=&color=181717&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="GitHub Logo" />
  </a>
  <img width="12" />
  <a href="mailto:vieiragabrieldesouza78@gmail.com">
    <img src="https://img.shields.io/static/v1?message=E-mail&logo=gmail&label=&color=D14836&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="Gmail Logo" />
  </a>
  <img width="12" />
  <a href="https://www.linkedin.com/in/SEU_LINKEDIN_AQUI">
    <img src="https://img.shields.io/static/v1?message=LinkedIn&logo=linkedin&label=&color=0077B5&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="LinkedIn Logo" />
  </a>
</div>

###

<p align="left">⭐ Fique à vontade para entrar em contato ou abrir issues!</p>
<div> <img style="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&reversal=false&fontSize=70&fontColor=FFFFFF&fontAlign=50&fontAlignY=50&stroke=-&descSize=20&descAlign=50&descAlignY=50&theme=cobalt" /> </div>
