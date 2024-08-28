import re
import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
import os

def check_driver_path(path):
    if not os.path.isfile(path):
        print(f"O caminho especificado não é um arquivo válido: {path}")
        return False
    if not os.access(path, os.X_OK):
        print(f"O arquivo não tem permissões de execução: {path}")
        return False
    print(f"O caminho do driver é válido e o arquivo é executável: {path}")
    return True

# Atualize o caminho do driver para o local correto
driver_path = 'C:/Users/HR/Documents/edgedriver/msedgedriver.exe'
if not check_driver_path(driver_path):
    raise ValueError(f"O caminho do driver não é válido ou o arquivo não é executável: {driver_path}")

service = EdgeService(executable_path=driver_path)

def fetch_page(url, use_proxy=False, use_selenium=False):
    print("Iniciando o WebDriver para o Edge...")
    edge_options = webdriver.EdgeOptions()
    if use_proxy:
        edge_options.add_argument('--proxy-server=your-proxy-url')
    
    driver = webdriver.Edge(service=service, options=edge_options)
    print(f"Acessando a URL: {url}")
    driver.get(url)
    
    time.sleep(random.uniform(5, 10))  # Adiciona um atraso aleatório para imitar o comportamento humano
    
    html = driver.page_source
    driver.quit()
    print("Página carregada e WebDriver encerrado.")
    return html

def remove_sensitive_info(html):
    print("Removendo informações sensíveis...")
    # Padrões de regex para nomes e CPFs
    name_pattern = re.compile(r'<[^>]*>\b[A-Z][a-z]* [A-Z][a-z]* [A-Z][a-z]* [A-Z][a-z]*\b<[^>]*>')
    cpf_pattern = re.compile(r'<[^>]*>\b\d{3}\.\d{3}\.\d{3}-\d{2}\b<[^>]*>')

    # Remover padrões encontrados e ajustar espaços em branco
    html = name_pattern.sub('', html)
    html = cpf_pattern.sub('', html)

    # Remover placeholders [REMOVED]
    html = re.sub(r'\[REMOVED\]', '', html)

    # Remover espaços em branco extras
    html = re.sub(r'\s+', ' ', html).strip()

    print("Informações sensíveis removidas.")
    return html

def save_cleaned_html(file_path, html):
    print(f"Salvando HTML limpo em {file_path}...")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    print("HTML limpo salvo com sucesso.")

def main():
    url = 'https://httpbin.org/ip'  # URL de teste corrigida
    output_file_path = 'cleaned_test.html'  # Caminho do arquivo HTML limpo
    print("Iniciando o processo de scraping...")
    html = fetch_page(url, use_proxy=False, use_selenium=False)  # Defina use_proxy=True para usar proxy, use_selenium=True para usar Selenium
    if html:
        cleaned_html = remove_sensitive_info(html)
        save_cleaned_html(output_file_path, cleaned_html)
        print(f"HTML limpo salvo em {output_file_path}")
    else:
        print("Falha ao obter o HTML da página.")

if __name__ == "__main__":
    main()