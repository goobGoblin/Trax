from album_fetcher import ReviewsFetcher

def fetch_genres(filename):
    """
    Read genres from a file, convert them to lowercase, remove spaces and hyphens, and exclude any genres that initially contained spaces.
    :param filename: str - Path to the file containing genres.
    :return: list - A list of genres, each converted to lowercase and without spaces or hyphens.
    """
    with open(filename, 'r') as file:
        genres = [
            line.strip().lower().replace(' ', '').replace('-', '')  # Remove spaces, hyphens, convert to lowercase, strip whitespace
            for line in file if line.strip()  # Ensure the line is not just whitespace
            and ' ' not in line.strip().lower()  # Exclude lines containing spaces before modification
        ]
    return genres


def get_genre_reviews(genre_name, review_type):
    print(f"Fetching reviews for genre: {genre_name}")
    reviews_fetcher = ReviewsFetcher(
        indices="REVIEW",
        language="ENGLISH",
        review_type=review_type,
        genre=genre_name,
        page=1,
        page_size=20
    )
    reviews_data = reviews_fetcher.fetch_reviews()
    if reviews_data:
        # Assuming you want to do something with the data, e.g., print or save
        reviews_fetcher.print_reviews_details(reviews_data)
        reviews_fetcher.save_review_details(reviews_data, genre_name, review_type)
        print(f"Data fetched for {genre_name}")
    else:
        print(f"No reviews found for the genre '{genre_name}'")

def genre_iterator(genres):
    for genre in genres:
        get_genre_reviews(genre, "ALBUM")

def main():
    genres = fetch_genres("genres.txt")  # Assuming this file exists with genres listed one per line
    genre_iterator(genres)
    #get_genre_reviews('acid', "ALBUM")

if __name__ == "__main__":
    main()