import pandas as pd
from sqlalchemy import create_engine, text


def inserirMysql(nomeTabela, df, db, metodo):


    engine = create_engine(f"mysql+pymysql://optaextract:*extractuser22@localhost/{db}?charset=utf8mb4")

    df.to_sql(nomeTabela, engine, if_exists=metodo, index=True)

def extrairMysql(nomeTabela ,db):


    engine = create_engine(f"mysql+pymysql://optaextract:*extractuser22@localhost/{db}")

    df = pd.read_sql(f"SELECT * FROM {nomeTabela}", con=engine)
    return df

def dropTable(nomeTabela, db):
    query = f"""
        DROP TABLE IF EXISTS `{nomeTabela}`;
        """
    engine = create_engine(f"mysql+pymysql://optaextract:*extractuser22@localhost/{db}?charset=utf8mb4")

    with engine.connect() as connection:

        connection.execute(text(query))