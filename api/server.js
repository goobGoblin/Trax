const express = require('express');
const mysql = require('mysql2');
const fs = require('fs');

const app = express();
const port = 5000;

const configData = fs.readFileSync('../config.json');
const config = JSON.parse(configData);

// Database configuration
const db_config = {
    host: config.host,
    user: config.user,
    password: config.password,
    database: config.database,
    port: config.port
};

// Create a MySQL connection pool
const pool = mysql.createPool(db_config);

// Test the database connection
pool.getConnection((err, connection) => {
    if (err) {
        console.error('Error connecting to database:', err);
        return;
    }

    console.log('Connected to the database.');

    // Get a list of tables in the database
    connection.query('SHOW TABLES', (err, results) => {
        connection.release();

        if (err) {
            console.error('Error querying tables:', err);
            return;
        }

        console.log('Tables in the database:');
        results.forEach(row => {
            console.log(row[`Tables_in_${db_config.database}`]);
        });
    });
});

// Route to test if the server is running
app.get('/', (req, res) => {
    res.send('Server is running.');
});

// Define route to handle the '/api/genres' endpoint
app.get('/genres', (req, res) => {
    // Perform a database query to retrieve genres from the database
    pool.query('SELECT * FROM Genres', (err, results) => {
        if (err) {
            console.error('Error querying genres:', err);
            res.status(500).send('Error querying genres');
            return;
        }
        // Send the fetched genres as JSON response
        res.json(results);
    });
});

app.get('/subgenres', (req, res) => {
    // Perform a database query to retrieve genres from the database
    pool.query('SELECT * FROM Subgenres', (err, results) => {
        if (err) {
            console.error('Error querying Subgenres:', err);
            res.status(500).send('Error querying Subgenres');
            return;
        }
        // Send the fetched genres as JSON response
        res.json(results);
    });
});

app.get('/genreSubgenre', (req, res) => {
    // Perform a database query to retrieve genres from the database
    pool.query('SELECT * FROM GenreSubgenre', (err, results) => {
        if (err) {
            console.error('Error querying genreSubgenre:', err);
            res.status(500).send('Error querying genreSubgenre');
            return;
        }
        // Send the fetched genres as JSON response
        res.json(results);
    });
});


app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
