import os
import time
import json
import random
import re
import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Imports para FIREFOX ---
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

class DataHarvester:
    def __init__(self):
        # 1. Configuração de Pastas
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_folder = os.path.join(base_dir, "exports")
        self.log_file = os.path.join(base_dir, "execution.log")
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"📁 Pasta de exportação: {self.output_folder}")

        # 2. Configuração de Logging (Arquivo + Console)
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        # Adiciona log no console também (opcional, para visualização em tempo real)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

        self.ua = UserAgent()
        self.session = requests.Session()

    def _get_random_headers(self):
        try:
            ua_random = self.ua.random
        except:
            ua_random = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"

        return {
            "User-Agent": ua_random,
            "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
            "Referer": "https://www.google.com/"
        }

    def _clean_text(self, text):
        if not text:
            return None
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _setup_selenium(self):
        """Configura o driver do FIREFOX (GeckoDriver)."""
        logging.info("Iniciando instância do Firefox...")
        
        firefox_options = Options()
        firefox_options.add_argument("--headless") # Roda sem janela
        
        try:
            firefox_options.set_preference("general.useragent.override", self.ua.random)
        except:
            pass

        try:
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
            return driver
        except Exception as e:
            logging.critical(f"Falha ao iniciar Firefox: {e}")
            print("\n❌ ERRO CRÍTICO: Firefox não encontrado ou erro no driver.")
            return None

    def _scroll_infinite(self, driver):
        logging.info("Executando scroll infinito...")
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            logging.warning(f"Falha durante o scroll: {e}")

    def fetch_data(self, url, use_selenium=False, scroll=False, retries=3):
        """
        Coleta dados com sistema de retentativa (Retry Logic).
        """
        logging.info(f"Iniciando coleta em: {url}")
        
        for attempt in range(retries):
            try:
                html_content = ""
                
                if use_selenium:
                    driver = self._setup_selenium()
                    if not driver: return None
                    
                    try:
                        driver.set_page_load_timeout(30) # Timeout de segurança
                        driver.get(url)
                        if scroll: self._scroll_infinite(driver)
                        html_content = driver.page_source
                    finally:
                        driver.quit()
                else:
                    # Modo Requests (Mais rápido)
                    time.sleep(random.uniform(1, 2))
                    response = self.session.get(url, headers=self._get_random_headers(), timeout=20)
                    response.raise_for_status()
                    response.encoding = 'utf-8'
                    html_content = response.text

                # Se chegou aqui, deu sucesso!
                return self._parse_html(html_content, url)

            except Exception as e:
                wait_time = (attempt + 1) * 2 # Backoff: espera 2s, 4s, 6s...
                logging.warning(f"Tentativa {attempt+1}/{retries} falhou para {url}. Erro: {e}")
                logging.info(f"Aguardando {wait_time}s antes de tentar novamente...")
                time.sleep(wait_time)
        
        logging.error(f"Falha definitiva ao coletar: {url}")
        return None

    def _parse_html(self, html, url):
        try:
            soup = BeautifulSoup(html, 'lxml')
        except:
            soup = BeautifulSoup(html, 'html.parser')
        
        data = {
            "metadata": {
                "url": url,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "title": self._clean_text(soup.title.string) if soup.title else "Sem Título",
                "description": "",
                "keywords": ""
            },
            "content": {
                "headings": [],
                "paragraphs": [],
                "links": [],
                "tables": [] 
            }
        }

        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_key = soup.find("meta", attrs={"name": "keywords"})
        if meta_desc: data["metadata"]["description"] = self._clean_text(meta_desc.get("content", ""))
        if meta_key: data["metadata"]["keywords"] = self._clean_text(meta_key.get("content", ""))

        for h in soup.find_all(['h1', 'h2', 'h3']):
            txt = self._clean_text(h.get_text())
            if txt: data["content"]["headings"].append({"tag": h.name, "text": txt})

        for p in soup.find_all('p'):
            txt = self._clean_text(p.get_text())
            if txt and len(txt) > 20: 
                data["content"]["paragraphs"].append(txt)

        for a in soup.find_all('a', href=True):
            href = a['href']
            txt = self._clean_text(a.get_text())
            if txt and href.startswith('http'):
                data["content"]["links"].append({"text": txt, "url": href})

        try:
            tables = pd.read_html(StringIO(str(soup)))
            for idx, df in enumerate(tables):
                tbl_clean = df.fillna("").to_dict(orient="records")
                data["content"]["tables"].append({f"table_{idx}": tbl_clean})
        except:
            pass 

        return data

    def save_results(self, data, filename_prefix="dataset"):
        if not data: return

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(self.output_folder, f"{filename_prefix}_{ts}.json")
        excel_path = os.path.join(self.output_folder, f"{filename_prefix}_{ts}.xlsx")

        # Salvar JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"JSON salvo: {json_path}")

        # Salvar Excel
        try:
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                pd.DataFrame([data["metadata"]]).to_excel(writer, sheet_name="Metadata", index=False)
                
                if data["content"]["links"]:
                    pd.DataFrame(data["content"]["links"]).to_excel(writer, sheet_name="Links", index=False)
                
                content_df = pd.DataFrame({
                    "Type": ["Heading"] * len(data["content"]["headings"]) + ["Paragraph"] * len(data["content"]["paragraphs"]),
                    "Content": [h["text"] for h in data["content"]["headings"]] + data["content"]["paragraphs"]
                })
                content_df.to_excel(writer, sheet_name="Conteudo_Texto", index=False)

                for idx, tbl_wrapper in enumerate(data["content"]["tables"]):
                    key = list(tbl_wrapper.keys())[0]
                    df_table = pd.DataFrame(tbl_wrapper[key])
                    df_table.to_excel(writer, sheet_name=f"Tabela_{idx}", index=False)
            
            logging.info(f"Excel salvo: {excel_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar Excel: {e}")

    def _get_domain_name(self, url):
        from urllib.parse import urlparse
        try:
            domain = urlparse(url).netloc
            return domain.replace('www.', '').replace('.', '_')
        except:
            return "site_unknown"

    def run_batch_parallel(self, file_path="urls.txt", use_selenium=False, max_workers=3):
        """
        Processamento em lote PARALELO (Multithreading).
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, file_path)

        if not os.path.exists(full_path):
            print(f"❌ Arquivo {full_path} não encontrado.")
            return

        with open(full_path, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]

        print(f"\n📦 Iniciando Data Harvester em MODO TURBO")
        print(f"🎯 Alvos: {len(urls)} URLs")
        print(f"⚡ Threads: {max_workers} simultâneas")
        print(f"🦊 Engine: {'Selenium/Firefox' if use_selenium else 'Requests (Rápido)'}")
        print("-" * 50)

        results_log = {"sucesso": [], "erro": []}

        # Função interna para ser usada pelas threads
        def process_one(url):
            try:
                data = self.fetch_data(url, use_selenium=use_selenium)
                if data:
                    domain = self._get_domain_name(url)
                    self.save_results(data, filename_prefix=domain)
                    return ("sucesso", url)
                else:
                    return ("erro", url)
            except Exception as e:
                logging.error(f"Erro fatal na thread {url}: {e}")
                return ("erro", url)

        # Gerenciador de Processos Paralelos
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(process_one, url): url for url in urls}
            
            for future in as_completed(future_to_url):
                status, url_proc = future.result()
                results_log[status].append(url_proc)
                print(f"🏁 [{status.upper()}] Finalizado: {url_proc}")

        print("\n📊 RELATÓRIO FINAL DO LOTE")
        print(f"✅ Sucessos: {len(results_log['sucesso'])}")
        print(f"❌ Falhas:   {len(results_log['erro'])}")
        logging.info("Processamento em lote finalizado.")

if __name__ == "__main__":
    bot = DataHarvester()
    
    print("\n--- DATA HARVESTER 3.0 (Firefox + Turbo Edition) ---")
    print("1 - Teste Único")
    print("2 - Lote TURBO (urls.txt)")
    
    mode = input("Opção: ").strip()

    if mode == "1":
        url = input("Cole a URL: ").strip() or "https://www.python.org"
        data = bot.fetch_data(url, use_selenium=False)
        bot.save_results(data, "teste_unico")
        
    elif mode == "2":
        sel_opt = input("Usar Selenium/Firefox? (s/n): ").lower()
        use_sel = True if sel_opt == 's' else False
        
        # Define limite de threads para não travar o PC
        # Se for Selenium, usa poucas (3). Se for Requests, usa muitas (8).
        workers = 3 if use_sel else 8
        
        bot.run_batch_parallel("urls.txt", use_selenium=use_sel, max_workers=workers)
        
    else:
        print("Opção inválida.")