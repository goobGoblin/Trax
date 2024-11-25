#With the sql username and password, and the name of the database tests, this script checks to see if the tables were created succesfuuly and has at least one tuple
USER=""
PASS=""
NAME=""

#All tables
TABLES=(
    "Users"
    "Artists"
    "Genres"
    "Subgenres"
    "GenreSubgenre"
    "Labels"
    "Albums"
    "AlbumGenres"
    "AlbumLabels"
    "Tracks"
    "DJMixes"
    "Follows"
)

#Checks if table exists and not empty
check_table() {
    local table_name=$1
    table_exists=$(mysql -u $USER -p$PASS -D $NAME -sse "SHOW TABLES LIKE '$table_name'")
    if [[ -z "$table_exists" ]]; then
        echo "'$table_name' does not exist."
        return
    fi

    #Checks if the table is not empty
    row_count=$(mysql -u $USER -p$PASS -D $NAME -sse "SELECT COUNT(*) FROM $table_name")
    if [[ "$row_count" -gt 0 ]]; then
        echo "'$table_name' exists"
    else
        echo "'$table_name' exists but has no rows."
    fi
}

echo "Checking tables in '$NAME'..."

for table in "${TABLES[@]}"; do
    check_table $table
done
