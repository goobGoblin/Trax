-- Link an artists to the genres and subgenres of their albums
CREATE VIEW ArtistsOverview AS
SELECT
    Artists.ArtistID,
    Artists.Name AS ArtistName,
    GROUP_CONCAT(DISTINCT Genres.Name ORDER BY Genres.Name SEPARATOR ', ') AS Genres,
    GROUP_CONCAT(DISTINCT Subgenres.Name ORDER BY Subgenres.Name SEPARATOR ', ') AS Subgenres,
    GROUP_CONCAT(DISTINCT Labels.Name ORDER BY Labels.Name SEPARATOR ', ') AS Labels,
    GROUP_CONCAT(DISTINCT Albums.Title ORDER BY Albums.ReleaseDate SEPARATOR ', ') AS Albums,
    GROUP_CONCAT(DISTINCT Tracks.Title ORDER BY Tracks.Title SEPARATOR ', ') AS Tracks,
    GROUP_CONCAT(DISTINCT DJMixes.Title ORDER BY DJMixes.ReleaseDate SEPARATOR ', ') AS DJMixes
FROM Artists
LEFT JOIN ArtistGenres ON Artists.ArtistID = ArtistGenres.ArtistID
LEFT JOIN Genres ON ArtistGenres.GenreID = Genres.GenreID
LEFT JOIN GenreSubgenres ON Genres.GenreID = GenreSubgenres.GenreID
LEFT JOIN Subgenres ON GenreSubgenres.SubgenreID = Subgenres.SubgenreID
LEFT JOIN ArtistLabels ON Artists.ArtistID = ArtistLabels.ArtistID
LEFT JOIN Labels ON ArtistLabels.LabelID = Labels.LabelID
LEFT JOIN Albums ON Artists.ArtistID = Albums.ArtistID
LEFT JOIN Tracks ON Artists.ArtistID = Tracks.ArtistID
LEFT JOIN DJMixes ON Artists.ArtistID = DJMixes.ArtistID
GROUP BY Artists.ArtistID, Artists.Name


-- EXAMPLE USAGE:
/*
SELECT ArtistName, GenreName, SubgenreName
FROM ArtistGenresView
WHERE ArtistName = 'Artist Name';
*/

-- Detailed albums view for easier album queries
CREATE VIEW DetailedAlbums AS
SELECT
    A.AlbumID,
    A.Title,
    A.ReleaseDate,
    A.recommended,  
    Artists.Name AS ArtistName,
    GROUP_CONCAT(DISTINCT Genres.Name ORDER BY Genres.Name SEPARATOR ', ') AS Genres,
    GROUP_CONCAT(DISTINCT Subgenres.SubgenreName ORDER BY Subgenres.SubgenreName SEPARATOR ', ') AS Subgenres,
    GROUP_CONCAT(DISTINCT Tracks.Title ORDER BY Tracks.Title SEPARATOR ', ') AS TrackList
FROM Albums A
LEFT JOIN Artists ON A.ArtistID = Artists.ArtistID
LEFT JOIN AlbumGenres ON A.AlbumID = AlbumGenres.AlbumID
LEFT JOIN Genres ON AlbumGenres.GenreID = Genres.GenreID
LEFT JOIN Subgenres ON AlbumGenres.SubgenreID = Subgenres.SubgenreID
LEFT JOIN Tracks ON A.AlbumID = Tracks.AlbumID
GROUP BY A.AlbumID;


-- EXAMPLE USAGE:
-- SELECT * FROM DetailedAlbums WHERE AlbumID = [Specific AlbumID];
