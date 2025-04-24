import csv

class Movie:
    def __init__(self, movie_id, title, director, genre, available, price):
        self.movie_id = movie_id
        self.title = title
        self.director = director
        self.genre = genre
        self.available = available
        self.price = price
        self.rental_count = 0

    def __str__(self):
        genre_names = ["Romance", "Thriller", "Animation", "Documentary", "Fantasy", "Action", "Sci-Fi", "Drama"]
        genre_name = genre_names[self.genre] if 0 <= self.genre < len(genre_names) else "Unknown"
        return f"{self.movie_id:<5} {self.title:<30} {self.director:<20} {genre_name:<12} {'Available' if self.available else 'Rented':<10} ${self.price:<6.2f} {self.rental_count}"

def load_movies(file_name):
    movies = []
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) < 6:
                    continue
                movie = Movie(
                    movie_id=row[0],
                    title=row[1],
                    director=row[2],
                    genre=int(row[3]),
                    available=row[4].strip().lower() == 'true',
                    price=float(row[5])
                )
                movies.append(movie)
    except FileNotFoundError:
        print(f"The catalog file ({file_name}) is not found")
        print("The movie library management system starts without catalog")
    return movies

def save_movies(file_name, movies):
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "Director", "Genre", "Available", "Price"])
            for movie in movies:
                writer.writerow([ 
                    movie.movie_id,
                    movie.title,
                    movie.director,
                    movie.genre,
                    str(movie.available),
                    f"{movie.price:.2f}"
                ])
    except Exception as e:
        print(f"Error saving movies: {e}")

def rent_movie(movies):
    movie_id = input("Enter the movie ID to rent: ").strip()
    for movie in movies:
        if movie.movie_id == movie_id:
            if not movie.available:
                print(f"'{movie.title}' is already rented")
                return
            movie.available = False
            movie.rental_count += 1
            print(f"You have successfully rented '{movie.title}'.")
            return
    print(f"Movie with ID {movie_id} not found.")

def return_movie(movies):
    movie_id = input("Enter the movie ID to return: ").strip()
    for movie in movies:
        if movie.movie_id == movie_id:
            if movie.available:
                print(f"'{movie.title}' was not rented.")
                return
            movie.available = True
            print(f"You have successfully returned '{movie.title}'.")
            return
    print(f"Movie with ID {movie_id} not found.")

def add_movie(movies):
    movie_id = input("Enter movie ID: ").strip()
    
    # Checking if the movie ID already exists
    for movie in movies:
        if movie.movie_id == movie_id:
            print(f"Movie with ID {movie_id} exists.")
            return
    
    title = input("Enter title: ").strip()
    director = input("Enter director: ").strip()
    print("Enter genre (0-9): \n0: Romance, 1: Thriller, 2: Animation, 3: Documentary, 4: Fantasy, 5: Action, 6: Sci-Fi, 7: Drama")
    genre = int(input("Enter genre number: ").strip())
    price = float(input("Enter price: ").strip())
    
    # Adding the movie
    new_movie = Movie(movie_id, title, director, genre, available=True, price=price)
    movies.append(new_movie)
    print(f"Movie '{title}' added successfully.")

def remove_movie(movies):
    movie_id = input("Enter the movie ID to remove: ").strip()
    for movie in movies:
        if movie.movie_id == movie_id:
            movies.remove(movie)
            print(f"Movie '{movie.title}' has been removed.")
            return
    print(f"Movie with ID {movie_id} not found.")

def list_movies_by_genre(movies):
    try:
        genre = int(input("Enter genre (0-9): ").strip())
        if genre < 0 or genre > 7:  # Ensuring the genre input is valid
            print("Invalid Genre: Enter a valid genre (0-7)")
            return
        
        genre_names = ["Romance", "Thriller", "Animation", "Documentary", "Fantasy", "Action", "Sci-Fi", "Drama"]
        genre_name = genre_names[genre]
        
        print(f"Movies in the genre '{genre_name}':")
        print(f"{'ID':<5} {'Title':<30} {'Director':<20} {'Genre':<12} {'Availability':<10} {'Price $':<8} {'Rental Count':<12}")
        print("-" * 85)
        
        matching_movies = [movie for movie in movies if movie.genre == genre]
        
        if not matching_movies:
            print(f"No movies found in the genre '{genre_name}'.")
        else:
            for movie in matching_movies:
                print(movie)
    except ValueError:
        print("Invalid input! Please enter a number for the genre.")

def top_rented_movies(movies):
    genre_names = ["Romance", "Thriller", "Animation", "Documentary", "Fantasy", "Action", "Sci-Fi", "Drama"]

    # Sort by rental_count in descending order
    top_movies = sorted(movies, key=lambda m: m.rental_count, reverse=True)[:5]

    print("Top 5 Rented Movies:")
    print(f"{'ID':<5} {'Title':<30} {'Director':<20} {'Genre':<12} {'Rentals':<8}")
    print("-" * 75)

    for movie in top_movies:
        genre_name = genre_names[movie.genre] if 0 <= movie.genre < len(genre_names) else "Unknown"
        print(f"{movie.movie_id:<5} {movie.title:<30} {movie.director:<20} {genre_name:<12} {movie.rental_count:<8}")
def check_availability_by_genre(movies):
    try:
        genre_names = ["Romance", "Thriller", "Animation", "Documentary", "Fantasy", "Action", "Sci-Fi", "Drama"]
        genre = int(input("Enter genre (0-7): ").strip())
        if genre < 0 or genre >= len(genre_names):
            print("Invalid Genre: Enter a valid genre (0-7)")
            return
        genre_name = genre_names[genre]
        print(f"\nMovies available in genre '{genre_name}':")
        print(f"{'ID':<5} {'Title':<30} {'Director':<20} {'Genre':<12} {'Availability':<12} {'Price $':<8} {'Rental Count':<12}")
        print("-" * 100)
        matching_movies = [m for m in movies if m.genre == genre and m.available]
        if not matching_movies:
            print(f"No available movies found in genre '{genre_name}'.")
        else:
            for movie in matching_movies:
                print(movie)
    except ValueError:
        print("Invalid input! Please enter a number for the genre.")

def print_menu():
    print("Movie Library - Main Menu")
    print("=" * 25)
    print("1) Search for movies")
    print("2) Rent a movie")
    print("3) Return a movie")
    print("4) Add a movie")
    print("5) Remove a movie")
    print("6) Update movie details")
    print("7) List movies by genre")
    print("8) Top rented movies")
    print("9) Check availability by genre")
    print("10) Display library summary")
    print("0) Exit the system")

    choice = input("Enter your selection: ")
    return choice

def display_summary(movies):
    total = len(movies)
    available = sum(1 for m in movies if m.available)
    rented = total - available
    print(f"Total movies: {total}")
    print(f"Available movies: {available}")
    print(f"Rented movies: {rented}")

def search_movies(movies):
    search_term = input("Enter search term: ").strip().lower()
    print(f"Finding ({search_term}) in title, director, or genre...")

    genre_names = ["Romance", "Thriller", "Animation", "Documentary", "Fantasy", "Action", "Sci-Fi", "Drama"]

    matching_movies = [
        movie for movie in movies
        if search_term in movie.title.lower() or
           search_term in movie.director.lower() or
           search_term in (genre_names[movie.genre] if 0 <= movie.genre < len(genre_names) else "Unknown").lower()
    ]

    if not matching_movies:
        print("No matching movies found.")
    else:
        print(f"{'ID':<5} {'Title':<30} {'Director':<20} {'Genre':<12} {'Availability':<10} {'Price $':<8} {'Rental Count':<12}")
        print("-" * 85)
        for movie in matching_movies:
            print(movie)

def update_movie_details(movies):
    movie_id = input("Enter the movie ID to update: ").strip()
    movie_found = False

    for movie in movies:
        if movie.movie_id == movie_id:
            movie_found = True
            print(f"Leave fields blank to keep current values.")
            
            new_title = input(f"Enter new title (current: {movie.title}): ").strip()
            if new_title:
                movie.title = new_title
            
            new_director = input(f"Enter new director (current: {movie.director}): ").strip()
            if new_director:
                movie.director = new_director
            
            print("Enter new genre (0-7): \n0: Romance, 1: Thriller, 2: Animation, 3: Documentary, 4: Fantasy, 5: Action, 6: Sci-Fi, 7: Drama")
            new_genre = input(f"Enter new genre (current: {movie.genre}): ").strip()
            if new_genre:
                new_genre = int(new_genre)
                if 0 <= new_genre <= 7:
                    movie.genre = new_genre
                else:
                    print("Invalid genre. Keeping current genre.")
            
            new_price = input(f"Enter new price (current: {movie.price}): ").strip()
            if new_price:
                try:
                    movie.price = float(new_price)
                except ValueError:
                    print("Invalid price. Keeping current price.")
            
            print(f"Movie with ID {movie_id} is updated successfully.")
            break
    
    if not movie_found:
        print(f"Movie with ID {movie_id} is not found.")

def main():
    file_name = input("Enter the movie catalog filename: ")
    movies = load_movies(file_name)

    while True:
        choice = print_menu()

        if choice == "0":
            confirm = input("Would you like to update the catalog (yes/y, no/n)? ").strip().lower()
            if confirm in ["yes", "y"]:
                save_movies(file_name, movies)
                print("Movie catalog has been updated. Goodbye!")
            else:
                print("Movie catalog has not been updated. Goodbye!")
            break

        elif choice == "1":
            search_movies(movies)

        elif choice == "2":
            rent_movie(movies)

        elif choice == "3":
            return_movie(movies)

        elif choice == "4":
            add_movie(movies)

        elif choice == "5":
            remove_movie(movies)

        elif choice == "6":
            update_movie_details(movies)

        elif choice == "7":
            list_movies_by_genre(movies)
        elif choice == "8":
           top_rented_movies(movies)
        elif choice == "9":
            check_availability_by_genre(movies)

        elif choice == "10":
            display_summary(movies)

        elif choice not in [str(i) for i in range(11)]:
            print("Invalid choice. Please try again.")

        else:
            print("[Feature not implemented in this test run]")

if __name__ == '__main__':
    main()




