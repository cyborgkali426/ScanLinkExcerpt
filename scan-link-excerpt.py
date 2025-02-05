import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def extract_links_with_pattern(base_url, pattern):
    """
    Extrai todos os links de um site que correspondem ao padrão fornecido.

    :param base_url: URL base do site (ex.: 'http://bancocn.com')
    :param pattern: Trecho de busca (ex.: '.php?id=')
    :return: Lista de URLs que contêm o padrão
    """
    visited_urls = set()  # Conjunto para armazenar URLs já visitadas
    matching_urls = set()  # Conjunto para armazenar URLs que correspondem ao padrão
    to_visit = [base_url]  # Fila de URLs a serem visitadas

    # Compila o padrão como uma expressão regular (insensível a maiúsculas/minúsculas)
    regex_pattern = re.compile(re.escape(pattern), re.IGNORECASE)

    while to_visit:
        current_url = to_visit.pop(0)  # Pega a próxima URL da fila
        if current_url in visited_urls:
            continue  # Ignora URLs já visitadas

        print(f"Visitando: {current_url}")
        visited_urls.add(current_url)

        try:
            # Faz a requisição HTTP
            response = requests.get(current_url, timeout=10)
            if response.status_code != 200:
                print(f"Erro ao acessar {current_url}: Status Code {response.status_code}")
                continue

            # Verifica se o padrão está presente na URL atual
            if regex_pattern.search(current_url):
                matching_urls.add(current_url)

            # Analisa o conteúdo HTML da página
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontra todos os links na página
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)  # Resolve URLs relativas

                # Garante que só adicionamos URLs do mesmo domínio
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    if full_url not in visited_urls and full_url not in to_visit:
                        to_visit.append(full_url)

        except Exception as e:
            print(f"Erro ao processar {current_url}: {e}")

    return matching_urls


if __name__ == "__main__":
    # Entrada do usuário
    host = input("Digite o host (ex.: http://bancocn.com): ").strip()
    search_pattern = input("Digite o trecho de busca (ex.: .php?id=): ").strip()

    # Executa a busca
    result = extract_links_with_pattern(host, search_pattern)

    # Exibe os resultados
    print("\nResultados encontrados:")
    if result:
        for url in result:
            print(url)
    else:
        print("Nenhum resultado encontrado.")