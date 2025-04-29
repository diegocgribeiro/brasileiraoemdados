from extract.ExtractOpta import pegarlinks, extrairTimes, pegarlinks_futuros
from extract.SQLUtils import inserirMysql
from extract.Tomados import rawTomados, fazerTabelaJogosTomados, timesGeralTomados
from extract.UnionTratamento import fazerTabelaSoma, timesGeral, fazerTabelaJogos

dfLinks = pegarlinks(0,  "https://optaplayerstats.statsperform.com/en_GB/soccer/serie-a-2025/9pqtmpr3w8jm73y0eb8hmum8k")
inserirMysql("links", dfLinks, "raw", "append")
extrairTimes()
fazerTabelaSoma()
timesGeral()
fazerTabelaJogos()
rawTomados()
fazerTabelaJogosTomados()
timesGeralTomados()
