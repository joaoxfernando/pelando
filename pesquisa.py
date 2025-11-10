import requests as req
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv
from datetime import datetime
from bot import enviar_mensagem as bot_msg, escapar_markdown as escape_md, escapar_html as escape_html
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Setup do driver
options = Options()
options.add_argument('--headless')  # Executar em modo headless (sem abrir janela)
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
url = 'https://www.pelando.com.br/recentes'
wait = WebDriverWait(driver, 15)
xpath_ofertas = '//main//ul/li//h3/a'
limite_ofertas = 20

# Ler itens no arquivo txt
arquivo_itens = os.getenv('itens_file')

with open(arquivo_itens, 'r', encoding='utf-8') as file:
    produtos_monitorados = [linha.strip() for linha in file if linha.strip()]


# Acessar a página
driver.get(url)
ofertas = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_ofertas)))

# Produto/termo que deseja monitorar
# produtos_monitorados = ['TV 55', 'Louças']
ofertas_dict = []

try:    
    # Iterar sobre as ofertas
    for oferta in ofertas[:20]: # limitar a 20 ofertas
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.2)
            # Encontrar título e link
            titulo = oferta.text
            link = oferta.get_attribute("href")
            hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # <- nova linha
            
            # salvando em um dicionário
            ofertas_dict.append({
                'data_hora': hora, 
                'título': titulo, 
                'link': link
            })

        except Exception as e:
            print(f'Erro ao processar oferta: {e}')
            continue

except Exception as e:
    print(f'Erro: {e}')

finally:
    driver.quit()

encontrados = [
    oferta for oferta in ofertas_dict 
    if any(produto.lower() in oferta['título'].lower() for produto in produtos_monitorados)
]

async def processar_encontrados(encontrados):
    if encontrados:
        print(f'Ofertas encontradas em {len(encontrados)} oferta(s):\n')
        await bot_msg(f'Foram encontradas {len(encontrados)} oferta(s) para o(s) produto(s) monitorado(s).')

        for oferta in encontrados:
            print(f"Título: {oferta['título']}")
            print(f"Link: {oferta['link']}")
            print('-' * 50)

            titulo = escape_html(oferta['título'])
            link = escape_html(oferta['link'])
            #🔗
            mensagem = (
                f"🛍️ <b>{titulo}</b>\n"
                f"🔗 <a href=\"{link}\">Clique aqui para ver a oferta</a>"
            )

            await bot_msg(mensagem)

        # Salvando ofertas encontradas em CSV
        file_csv = 'ofertas_encontradas.csv'
        with open(file_csv, mode='a', newline='', encoding='utf-8') as file:
            fields = ['data_hora', 'título', 'link']
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for oferta in encontrados:
                writer.writerow(oferta)
        print(f'As ofertas encontradas foram salvas em {file_csv}.')
    else:
        print('Nenhuma oferta encontrada para o(s) produto(s) monitorado(s).')

if __name__ == '__main__':
    asyncio.run(processar_encontrados(encontrados))