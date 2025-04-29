const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'optaextract', // Altere para o seu usuário MySQL
    password: '*extractuser22', // Altere para a sua senha MySQL
    database: 'refinedgeral'
});

connection.connect(err => {
    if (err) {
        console.error('Erro ao conectar ao MySQL: ', err.stack);
    }
    console.log('Conectado ao banco de dados MySQL');
});

const connection2 = mysql.createConnection({
    host: 'localhost',
    user: 'optaextract', // Altere para o seu usuário MySQL
    password: '*extractuser22', // Altere para a sua senha MySQL
    database: 'refinedjogadores'
});

connection2.connect(err => {
    if (err) {
        console.error('Erro ao conectar ao MySQL: ', err.stack);
    }
    console.log('Conectado ao banco de dados MySQL');
});


app.get('/match-data', (req, res) => {
    const { homeTeam, awayTeam } = req.query;

    const query1 = 'SELECT * FROM timesgeral WHERE Equipe = ? union SELECT * FROM timesmandante WHERE Equipe = ? union SELECT * FROM timesgeraltomados WHERE Adversário = ? union SELECT * FROM timestomadosmandante WHERE Adversário = ? union SELECT * FROM timestomadosvisitante WHERE Adversário = ? union SELECT * FROM timesvisitante WHERE Equipe = ?';
    const query2 = 'SELECT * FROM timesgeral WHERE Equipe = ? union SELECT * FROM timesvisitante WHERE Equipe = ? union SELECT * FROM timesgeraltomados WHERE Adversário = ? union SELECT * FROM timestomadosvisitante WHERE Adversário = ? union SELECT * FROM timestomadosmandante WHERE Adversário = ? union SELECT * FROM timesmandante WHERE Equipe = ?';
    Promise.all([
        new Promise((resolve, reject) => {
            connection.query(query1,[homeTeam, homeTeam, homeTeam, homeTeam, homeTeam, homeTeam], (err, results1) => {
                if (err) {
                    console.error('Erro na primeira consulta: ', err);
                    reject(err);
                    return;
                }
                resolve(results1);
            });
        }),
        new Promise((resolve, reject) => {
            connection.query(query2, [awayTeam, awayTeam, awayTeam, awayTeam, awayTeam, awayTeam],(err, results2) => {
                if (err) {
                    console.error('Erro na segunda consulta: ', err);
                    reject(err);
                    return;
                }
                resolve(results2);
            });
        })
    ])
        .then(([results1, results2]) => {
            // Combine the results into a single object
            const combinedResults = {
                data1: results1,
                data2: results2
            };
            res.json(combinedResults);
        })
        .catch(error => {
            console.error('Erro ao executar as consultas: ', error);
            res.status(500).send('Erro ao acessar dados do banco de dados');
        });
});

app.get('/player-stats', (req, res) => {
    const { homeTeam, awayTeam } = req.query;

    const query1 = `SELECT * FROM \`${homeTeam.toLowerCase()}\``;;
    const query2 = `SELECT * FROM \`${awayTeam.toLowerCase()}\``;
        Promise.all([
        new Promise((resolve, reject) => {
            connection2.query(query1,[homeTeam.toLowerCase()], (err, results1) => {
                if (err) {
                    console.error('Erro na primeira consulta: ', err);
                    reject(err);
                    return;
                }
                resolve(results1);
            });
        }),
        new Promise((resolve, reject) => {
            connection2.query(query2, [awayTeam.toLowerCase()],(err, results2) => {
                if (err) {
                    console.error('Erro na segunda consulta: ', err);
                    reject(err);
                    return;
                }
                resolve(results2);
            });
        })
    ])
        .then(([results1, results2]) => {
            // Combine the results into a single object
            const combinedResults = {
                data1: results1,
                data2: results2
            };
            res.json(combinedResults);
        })
        .catch(error => {
            console.error('Erro ao executar as consultas: ', error);
            res.status(500).send('Erro ao acessar dados do banco de dados');
        });
});

app.use(express.static('public'));

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
