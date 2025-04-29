import pandas as pd
from warnings import simplefilter
from sqlalchemy import create_engine, text
import warnings

from SQLUtils import inserirMysql, dropTable

warnings.simplefilter(action='ignore', category=FutureWarning)
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)



def fazerTabelaSoma():

    tabelas = ['Botafogo FR', 'CA Mineiro', 'CR Flamengo', 'CR Vasco da Gama', 'Ceará SC', 'Cruzeiro EC', 'EC Bahia',
     'EC Juventude', 'EC Vitória', 'Fluminense FC', 'Fortaleza EC', 'Grêmio FB Porto Alegrense', 'Mirassol FC',
     'Red Bull Bragantino', 'São Paulo FC', 'SC Corinthians Paulista', 'SC Internacional', 'SC do Recife', 'SE Palmeiras', 'Santos FC Sao Paulo']

    for tabela in tabelas:
        tabela = tabela.lower()
        dropTable(tabela, "refinedjogadores")
        print("Tabela excluida com sucesso")
        query = f"""
                
                
                CREATE TABLE `refinedjogadores`.`{tabela}` AS
                SELECT 
                    `Atleta`, -- Nome do jogador
                    SUM(`Gols`) AS `Gols`,
                    SUM(`Assistência`) AS `Assistência`,
                    SUM(`Cartão Vermelho`) AS `Cartão Vermelho`,
                    SUM(`Cartão Amarelo`) AS `Cartão Amarelo`,
                    SUM(`Escanteios`) AS `Escanteios`,
                    SUM(`Chutes`) AS `Chutes`,
                    SUM(`Chutes no Gol`) AS `Chutes no Gol`,
                    SUM(`Chutes Bloqueados`) AS `Chutes Bloqueados`,
                    SUM(`Passes`) AS `Passes`,
                    SUM(`Cruzamentos`) AS `Cruzamentos`,
                    SUM(`Roubada de Bola`) AS `Roubada de Bola`,
                    SUM(`Impedimentos`) AS `Impedimentos`,
                    SUM(`Faltas Concedidas`) AS `Faltas Concedidas`,
                    SUM(`Faltas Ganhas`) AS `Faltas Ganhas`,
                    SUM(`Defesas`) AS `Defesas`,
                    COUNT(*) AS `Jogos`,
                    `Equipe`
                FROM 
                    `raw`.`{tabela}`
                GROUP BY 
                    `Atleta`;
                """
        engine = create_engine(f"mysql+pymysql://optaextract:*extractuser22@localhost/refinedjogadores?charset=utf8mb4")
        with engine.connect() as connection:

            connection.execute(text(query))

        print("Tabela criada com sucesso")



def timesGeral():

    tabelas = ['Botafogo FR', 'CA Mineiro', 'CR Flamengo', 'CR Vasco da Gama', 'Ceará SC', 'Cruzeiro EC', 'EC Bahia',
               'EC Juventude', 'EC Vitória', 'Fluminense FC', 'Fortaleza EC', 'Grêmio FB Porto Alegrense', 'Mirassol FC',
               'Red Bull Bragantino', 'São Paulo FC', 'SC Corinthians Paulista', 'SC Internacional', 'SC do Recife', 'SE Palmeiras', 'Santos FC Sao Paulo']

    engine = create_engine("mysql+pymysql://optaextract:*extractuser22@localhost/raw?charset=utf8mb4")
    dataframes = []


    for tabela in tabelas:
        tabela = tabela.lower()
        query = f"""
                
                
                SELECT 
                    `Equipe`, -- Nome do jogador
                    SUM(`Gols`) AS `Gols`,
                    SUM(`Assistência`) AS `Assistência`,
                    SUM(`Cartão Vermelho`) AS `Cartão Vermelho`,
                    SUM(`Cartão Amarelo`) AS `Cartão Amarelo`,
                    SUM(`Escanteios`) AS `Escanteios`,
                    SUM(`Chutes`) AS `Chutes`,
                    SUM(`Chutes no Gol`) AS `Chutes no Gol`,
                    SUM(`Chutes Bloqueados`) AS `Chutes Bloqueados`,
                    SUM(`Passes`) AS `Passes`,
                    SUM(`Cruzamentos`) AS `Cruzamentos`,
                    SUM(`Roubada de Bola`) AS `Roubada de Bola`,
                    SUM(`Impedimentos`) AS `Impedimentos`,
                    SUM(`Faltas Concedidas`) AS `Faltas Concedidas`,
                    SUM(`Faltas Ganhas`) AS `Faltas Ganhas`,
                    SUM(`Defesas`) AS `Defesas`,
                    COUNT(DISTINCT `Adversário`) AS `Jogos`
                FROM 
                    `raw`.`{tabela}`
                """
        df = pd.read_sql(query, engine)
        dataframes.append(df)

# Concatenar todos os DataFrames em um único
    tabela_consolidada = pd.concat(dataframes)
    dropTable("timesgeral", "refinedgeral")
# Salvar a tabela consolidada no banco de dados ou em um arquivo CSV]
    inserirMysql("timesgeral", tabela_consolidada, "refinedgeral", "replace")

    for local in ("Mandante", "Visitante"):
        dataframes = []
        for tabela in tabelas:
            tabela = tabela.lower()
            query = f"""
                    
                    
                    SELECT 
                        `Equipe`, -- Nome do jogador
                        SUM(`Gols`) AS `Gols`,
                        SUM(`Assistência`) AS `Assistência`,
                        SUM(`Cartão Vermelho`) AS `Cartão Vermelho`,
                        SUM(`Cartão Amarelo`) AS `Cartão Amarelo`,
                        SUM(`Escanteios`) AS `Escanteios`,
                        SUM(`Chutes`) AS `Chutes`,
                        SUM(`Chutes no Gol`) AS `Chutes no Gol`,
                        SUM(`Chutes Bloqueados`) AS `Chutes Bloqueados`,
                        SUM(`Passes`) AS `Passes`,
                        SUM(`Cruzamentos`) AS `Cruzamentos`,
                        SUM(`Roubada de Bola`) AS `Roubada de Bola`,
                        SUM(`Impedimentos`) AS `Impedimentos`,
                        SUM(`Faltas Concedidas`) AS `Faltas Concedidas`,
                        SUM(`Faltas Ganhas`) AS `Faltas Ganhas`,
                        SUM(`Defesas`) AS `Defesas`,
                        COUNT(DISTINCT `Adversário`) AS `Jogos`
                    FROM 
                        `raw`.`{tabela}`
                    WHERE `Mandante ou Visitante` = '{local}'
                    """
            df = pd.read_sql(query, engine)
            dataframes.append(df)

        # Concatenar todos os DataFrames em um único
        tabela_consolidada = pd.concat(dataframes)
        dropTable(f"Times{local}", "refinedgeral")
        # Salvar a tabela consolidada no banco de dados ou em um arquivo CSV]
        inserirMysql(f"Times{local}", tabela_consolidada, "refinedgeral", "replace")



def fazerTabelaJogos():

    tabelas = ['Botafogo FR', 'CA Mineiro', 'CR Flamengo', 'CR Vasco da Gama', 'Ceará SC', 'Cruzeiro EC', 'EC Bahia',
               'EC Juventude', 'EC Vitória', 'Fluminense FC', 'Fortaleza EC', 'Grêmio FB Porto Alegrense', 'Mirassol FC',
               'Red Bull Bragantino', 'São Paulo FC', 'SC Corinthians Paulista', 'SC Internacional', 'SC do Recife', 'SE Palmeiras', 'Santos FC Sao Paulo']

    for tabela in tabelas:
        tabela = tabela.lower()
        dropTable(tabela, "refinedjogos")
        print("Tabela excluida com sucesso")
        query = f"""
                
                
                CREATE TABLE `refinedjogos`.`{tabela}` AS
                SELECT 
                    `Equipe`, -- Nome do jogador
                    SUM(`Gols`) AS `Gols`,
                    SUM(`Assistência`) AS `Assistência`,
                    SUM(`Cartão Vermelho`) AS `Cartão Vermelho`,
                    SUM(`Cartão Amarelo`) AS `Cartão Amarelo`,
                    SUM(`Escanteios`) AS `Escanteios`,
                    SUM(`Chutes`) AS `Chutes`,
                    SUM(`Chutes no Gol`) AS `Chutes no Gol`,
                    SUM(`Chutes Bloqueados`) AS `Chutes Bloqueados`,
                    SUM(`Passes`) AS `Passes`,
                    SUM(`Cruzamentos`) AS `Cruzamentos`,
                    SUM(`Roubada de Bola`) AS `Roubada de Bola`,
                    SUM(`Impedimentos`) AS `Impedimentos`,
                    SUM(`Faltas Concedidas`) AS `Faltas Concedidas`,
                    SUM(`Faltas Ganhas`) AS `Faltas Ganhas`,
                    SUM(`Defesas`) AS `Defesas`,
                    `Data`,
                    `Link`,
                    `Adversário`,
                    `Mandante ou Visitante`
                FROM 
                    `raw`.`{tabela}`
                GROUP BY 
                    `Adversário`;
                """
        engine = create_engine(f"mysql+pymysql://optaextract:*extractuser22@localhost/refinedjogos?charset=utf8mb4")

        with engine.connect() as connection:

            connection.execute(text(query))

        print("Tabela criada com sucesso")






