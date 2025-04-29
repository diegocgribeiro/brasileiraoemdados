import pandas as pd
from warnings import simplefilter
from sqlalchemy import create_engine, text
import warnings

from SQLUtils import inserirMysql, dropTable

warnings.simplefilter(action='ignore', category=FutureWarning)
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

def rawTomados():

    tabelas = ['Botafogo FR', 'CA Mineiro', 'CR Flamengo', 'CR Vasco da Gama', 'Ceará SC', 'Cruzeiro EC', 'EC Bahia',
               'EC Juventude', 'EC Vitória', 'Fluminense FC', 'Fortaleza EC', 'Grêmio FB Porto Alegrense', 'Mirassol FC',
               'Red Bull Bragantino', 'São Paulo FC', 'SC Corinthians Paulista', 'SC Internacional', 'SC do Recife', 'SE Palmeiras', 'Santos FC Sao Paulo']

    engine = create_engine("mysql+pymysql://optaextract:*extractuser22@localhost/raw?charset=utf8mb4")

    for tabela in tabelas:
        dataframes = []
        for tabela2 in tabelas:
            tabela2 = tabela2.lower()
            query = f"""
                    SELECT 
                        `Equipe`,
                        `Atleta`,-- Nome do jogador
                        `Gols`,
                        `Assistência`,
                        `Cartão Vermelho`,
                        `Cartão Amarelo`,
                        `Escanteios`,
                        `Chutes`,
                        `Chutes no Gol`,
                        `Chutes Bloqueados`,
                        `Passes`,
                        `Cruzamentos`,
                        `Roubada de Bola`,
                        `Impedimentos`,
                        `Faltas Concedidas`,
                        `Faltas Ganhas`,
                        `Defesas`,
                        `Adversário`,
                        `Data`,
                        CASE
                            WHEN `Mandante ou Visitante` = 'Mandante' THEN 'Visitante'
                            WHEN `Mandante ou Visitante` = 'Visitante' THEN 'Mandante'
                            ELSE `Mandante ou Visitante`
                        END as `Mandante ou Visitante`,
                        `Link`
                    FROM 
                        `raw`.`{tabela2}`
                    WHERE `Adversário` = '{tabela}'
                    """
            df = pd.read_sql(query, engine)
            dataframes.append(df)

        # Concatenar todos os DataFrames em um único
        tabela_consolidada = pd.concat(dataframes)

        dropTable(tabela.lower(), "rawtomados")
        # Salvar a tabela consolidada no banco de dados ou em um arquivo CSV]
        inserirMysql(tabela.lower(), tabela_consolidada, "rawtomados", "replace")

def fazerTabelaJogosTomados():

    tabelas = ['Botafogo FR', 'CA Mineiro', 'CR Flamengo', 'CR Vasco da Gama', 'Ceará SC', 'Cruzeiro EC', 'EC Bahia',
               'EC Juventude', 'EC Vitória', 'Fluminense FC', 'Fortaleza EC', 'Grêmio FB Porto Alegrense', 'Mirassol FC',
               'Red Bull Bragantino', 'São Paulo FC', 'SC Corinthians Paulista', 'SC Internacional', 'SC do Recife', 'SE Palmeiras', 'Santos FC Sao Paulo']

    for tabela in tabelas:
        tabela = tabela.lower()
        dropTable(tabela, "refinedjogostomados")
        print("Tabela excluida com sucesso")
        query = f"""
                
                
                CREATE TABLE `refinedjogostomados`.`{tabela}` AS
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
                    `rawtomados`.`{tabela}`
                GROUP BY 
                    `Equipe`;
                """
        engine = create_engine(f"mysql+pymysql://optaextract:*extractuser22@localhost/refinedjogostomados?charset=utf8mb4")

        with engine.connect() as connection:

            connection.execute(text(query))

        print("Tabela criada com sucesso")

def timesGeralTomados():

    tabelas = ['Botafogo FR', 'CA Mineiro', 'CR Flamengo', 'CR Vasco da Gama', 'Ceará SC', 'Cruzeiro EC', 'EC Bahia',
               'EC Juventude', 'EC Vitória', 'Fluminense FC', 'Fortaleza EC', 'Grêmio FB Porto Alegrense', 'Mirassol FC',
               'Red Bull Bragantino', 'São Paulo FC', 'SC Corinthians Paulista', 'SC Internacional', 'SC do Recife', 'SE Palmeiras', 'Santos FC Sao Paulo']

    engine = create_engine("mysql+pymysql://optaextract:*extractuser22@localhost/raw?charset=utf8mb4")
    dataframes = []


    for tabela in tabelas:
        tabela = tabela.lower()
        query = f"""
                
                SELECT 
                    `Adversário`, 
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
                    COUNT(DISTINCT `Equipe`) AS `Jogos`
                FROM 
                    `rawtomados`.`{tabela}`
                """
        df = pd.read_sql(query, engine)
        dataframes.append(df)

    # Concatenar todos os DataFrames em um único
    tabela_consolidada = pd.concat(dataframes)
    dropTable("timesgeraltomados", "refinedgeral")
    # Salvar a tabela consolidada no banco de dados ou em um arquivo CSV]
    inserirMysql("timesgeraltomados", tabela_consolidada, "refinedgeral", "replace")

    for local in ("Mandante", "Visitante"):
        dataframes = []
        for tabela in tabelas:
            tabela = tabela.lower()
            query = f"""
                    
                    
                    SELECT 
                        `Adversário`, -- Nome do jogador
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
                        COUNT(DISTINCT `Equipe`) AS `Jogos`
                    FROM 
                        `rawtomados`.`{tabela}`
                    WHERE `Mandante ou Visitante` = '{local}'
                    """
            df = pd.read_sql(query, engine)
            dataframes.append(df)

        # Concatenar todos os DataFrames em um único
        tabela_consolidada = pd.concat(dataframes)
        dropTable(f"timestomados{local}", "refinedgeral")
        # Salvar a tabela consolidada no banco de dados ou em um arquivo CSV]
        inserirMysql(f"timestomados{local}", tabela_consolidada, "refinedgeral", "replace")

