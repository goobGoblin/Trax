// routes/albumRoutes.js
const express = require('express');
const router = express.Router();

module.exports = (connection) => {
    // Endpoint to fetch albums with optional genre and year filters
    router.get('/basic-albums', (req, res) => {
        const { genreID, year, recommended } = req.query;
        let query = 'SELECT Albums.AlbumID, Albums.Title, Albums.ArtistID, Genres.Name AS GenreName FROM Albums JOIN AlbumGenres ON Albums.AlbumID = AlbumGenres.AlbumID JOIN Genres ON AlbumGenres.GenreID = Genres.GenreID WHERE 1 = 1';
        const params = [];

        if (genreID) {
            query += ' AND Genres.GenreID = ?';
            params.push(genreID);
        }

        if (year) {
            query += ' AND YEAR(Albums.ReleaseDate) = ?';
            params.push(year);
        }

        
        if (recommended) {
            query += ' AND Albums.recommended = ?';
            params.push(recommended);
        }

        connection.query(query, params, (error, results) => {
            if (error) {
                res.status(500).json({ error: 'Internal server error', details: error });
            } else {
                res.json(results);
            }
        });
    });


    return router;
}