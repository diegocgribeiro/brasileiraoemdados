from datetime import datetime

import numpy as np
from selenium.webdriver.common.by import By
import time
import pandas as pd
import undetected_chromedriver as uc

from warnings import simplefilter

from sqlalchemy import create_engine
import warnings
import os

from SQLUtils import inserirMysql, extrairMysql

warnings.simplefilter(action='ignore', category=FutureWarning)
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

script_dir = os.path.dirname(os.path.abspath(__file__))



def pegarlinks(atualizacao, link):
    driver = uc.Chrome()
    linksantigos = extrairMysql("Links", "raw")['Links'].tolist()
    todos_links = []
    campeonato = link

    driver.get(campeonato +'/opta-player-stats')
    time.sleep(5)
    links = driver.find_elements(By.XPATH,'//tbody[@data-period="FullTime"]')
    for link in links:
        id = (link.get_attribute("data-match"))
        link3 = campeonato+'/match/view/'+id+'/match-summary'
        if link3 not in linksantigos:
            todos_links.append(link3)
    driver.quit()
    df = pd.DataFrame(todos_links, columns=["links"])
    return df

def extrairTimes():
    driver = uc.Chrome()
    linksacessados = extrairMysql("linksacessados", "raw")['Links'].tolist()
    linksExtraidos = extrairMysql("links", "raw")['Links'].tolist()
    for link in linksExtraidos:
        if link not in linksacessados:
            linksacessadosAgora = []
            linksacessadosAgora.append(link)
            driver.get(link)
            time.sleep(5)
            driver.execute_script("document.body.style.zoom='40%'")
            time.sleep(3)

            horario = driver.find_element(By.XPATH,'//*[@id="Opta_0"]/div/div/table/tbody/tr[2]/td/div/span[2]').text
            data_formatada = datetime.strptime(horario, "%d %B %Y %H:%M")

            driver.find_element(By.XPATH,'//*[@id="Opta_2"]/div/div/div[1]/div/ul/li[2]').click()
            equipea = driver.find_element(By.XPATH,'//*[@id="Opta_0"]/div/div/table/tbody/tr[1]/td[2]').text
            equipeb = driver.find_element(By.XPATH,'//*[@id="Opta_0"]/div/div/table/tbody/tr[1]/td[6]').text
            trs = driver.find_elements(By.XPATH, "//tr[@role='row']")
            trs = trs[:-1]
            data = []
            for tr in trs:
            # Localizar todas as células <td> dentro da linha
                th = tr.find_element(By.TAG_NAME, "th").text  # Captura o nome do atleta
                tds = [td.text for td in tr.find_elements(By.TAG_NAME, "td")]  # Captura outras colunas
                row = [th] + tds  # Combinar o conteúdo do <th> com os <td>
                data.append(row)
            df = pd.DataFrame(data, columns=['Atleta','Gols', 'Assistência', 'Cartão Vermelho', 'Cartão Amarelo', 'Escanteios', 'Chutes', 'Chutes no Gol', 'Chutes Bloqueados', 'Passes', 'Cruzamentos', 'Roubada de Bola', 'Impedimentos', 'Faltas Concedidas', 'Faltas Ganhas', 'Defesas'])
            df = df.replace(r"^\s*$", np.nan, regex=True)
            df = df.dropna(how="all")
            df.reset_index(drop=True, inplace=True)
            df.index += 1
            df["Equipe"] = equipea
            df["Data"] = data_formatada
            df["Adversário"] = equipeb
            df["Mandante ou Visitante"] = "Mandante"
            df["Link"] = link


            time.sleep(3)

            driver.find_element(By.XPATH,'//*[@id="Opta_2"]/div/div/div[1]/div/ul/li[3]').click()

            trs = driver.find_elements(By.XPATH, "//tr[@role='row']")
            trs = trs[:-1]
            data = []
            for tr in trs:
                # Localizar todas as células <td> dentro da linha
                th = tr.find_element(By.TAG_NAME, "th").text  # Captura o nome do atleta
                tds = [td.text for td in tr.find_elements(By.TAG_NAME, "td")]  # Captura outras colunas
                row = [th] + tds  # Combinar o conteúdo do <th> com os <td>
                data.append(row)
            df2 = pd.DataFrame(data, columns=['Atleta','Gols', 'Assistência', 'Cartão Vermelho', 'Cartão Amarelo', 'Escanteios', 'Chutes', 'Chutes no Gol', 'Chutes Bloqueados', 'Passes', 'Cruzamentos', 'Roubada de Bola', 'Impedimentos', 'Faltas Concedidas', 'Faltas Ganhas', 'Defesas'])
            df2 = df2.replace(r"^\s*$", np.nan, regex=True)
            df2 = df2.dropna(how="all")
            df2.reset_index(drop=True, inplace=True)
            df2.index += 1
            df2["Equipe"] = equipeb
            df2["Data"] = data_formatada
            df2["Adversário"] = equipea
            df2["Mandante ou Visitante"] = "Visitante"
            df2["Link"] = link

            inserirMysql(equipea.lower(), df, "raw", "append")
            inserirMysql(equipeb.lower(), df2, "raw", "append")
            df = pd.DataFrame(linksacessadosAgora, columns=['links'])
            inserirMysql("linksacessados", df, "raw", "append")


def pegarlinks_futuros(link):
    driver = uc.Chrome()
    todos_links = []
    campeonato = link
    driver.get(campeonato +'/fixtures')
    time.sleep(5)
    links = driver.find_elements(By.XPATH,'//li[@class="Opta-On"]//tbody[@data-period="PreMatch"]')
    for link in links:
        id = (link.get_attribute("data-match"))
        todos_links.append(campeonato+'/match/view/'+id+'/match-preview')
    data = []
    for link in todos_links:
        driver.get(link)
        time.sleep(3)
        time_a = driver.find_element(By.XPATH,'//*[@id="Opta_0"]/div/div/table/tbody/tr[1]/td[2]').text
        time_b = driver.find_element(By.XPATH,'//*[@id="Opta_0"]/div/div/table/tbody/tr[1]/td[6]').text
        row = [time_a, time_b, link] # Combinar o conteúdo do <th> com os <td>
        data.append(row)
    print(data)
    if len(data) ==  0:
        print("Optajoe ainda não lançou a proxima rodada")
        return "Optajoe ainda não lançou a proxima rodada"
    else:
        df = pd.DataFrame(data, columns=['Time A', 'Time B', 'Link'])
        return df


