class Movie:
    def __init__(self, title, show_time, rows, cols, price_per_ticket):
        self.title = title
        self.show_time = show_time
        self.rows = rows
        self.cols = cols
        self.seats = [[True] * cols for _ in range(rows)]  # Initialize all seats as available
        self.price_per_ticket = price_per_ticket

    def get_available_seats(self):
        available_seats = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.seats[row][col]:
                    available_seats.append(f"Row {row+1}, Seat {col+1}")
        return available_seats

    def display_seats(self):
        print(f"Seat Layout for {self.title} at {self.show_time}:")
        seat_num = 1
        for row in self.seats:
            row_str = ""
            for seat in row:
                row_str += f"  {seat_num:2d}  " if seat else "  B   " 
                seat_num += 1
            print(row_str)

    def book_seat(self, seat_number):
        """
        Books a seat by its absolute seat number.

        Args:
          seat_number: The absolute seat number to be booked (1-indexed).

        Returns:
          True if the seat was successfully booked, False otherwise.
        """
        if 1 <= seat_number <= self.rows * self.cols:
            row = (seat_number - 1) // self.cols  # Calculate row index
            col = (seat_number - 1) % self.cols  # Calculate column index

            if self.seats[row][col]:
                self.seats[row][col] = False
                return True
        return False

class Theater:
    def __init__(self, name, movies):
        self.name = name
        self.movies = movies

class BookingSystem:
    def __init__(self):
        self.theaters = {
            "Asian Sridevi": Theater("Asian Sridevi", [
                Movie("Pushpa-2", "10:00 AM", 10, 10, 150),
                Movie("Pushpa-2", "02:00 PM", 10, 10, 150),
                Movie("Mufasa: The Lion King", "02:00 PM", 8, 12, 120) 
            ]),
            "PVR": Theater("PVR", [
                Movie("Pushpa-2", "01:00 PM", 12, 8, 180),
                Movie("The Dark Knight", "07:00 PM", 10, 10, 150)
            ])
        }

        self.all_movies = set()  # Create a set to store all unique movie titles
        for theater in self.theaters.values():
            for movie in theater.movies:
                self.all_movies.add(movie.title)

    def user_login(self):
        print("Welcome to the Movie Booking System!")
        user_type = input("Login as (User/Admin): ").lower()

        if user_type == "user":
            self.user_booking()
        elif user_type == "admin":
            # Implement admin functionalities (e.g., add movies, update show times)
            print("Admin functionalities are not implemented yet.")
        else:
            print("Invalid input. Please enter 'User' or 'Admin'.")

    def user_booking(self):
        while True: 
            user_name = input("Enter your Name: ")
            user_phone = input("Enter your Phone Number: ")

            print("\nAvailable Movies:")
            for i, movie_title in enumerate(self.all_movies):
                print(f"{i+1}. {movie_title}")

            movie_choice = int(input("Select a movie (enter number): ")) - 1
            if 0 <= movie_choice < len(self.all_movies):
                selected_movie_title = list(self.all_movies)[movie_choice]

                print("\nAvailable Theaters for", selected_movie_title)
                available_theaters = [theater for theater in self.theaters.values() 
                                     for movie in theater.movies if movie.title == selected_movie_title]
                for i, theater in enumerate(available_theaters):
                    print(f"{i+1}. {theater.name}")

                theater_choice = int(input("Select a theater ( enter number ): ")) - 1
                if 0 <= theater_choice < len(available_theaters):
                    selected_theater = available_theaters[theater_choice] 
                    print("\nAvailable Showtimes for", selected_movie_title, "at", selected_theater.name)
                    for movie in selected_theater.movies:
                        if movie.title == selected_movie_title:
                            print(f"- {movie.show_time}") 
                    show_time_choice = input("Select a showtime: ") 
                    selected_movie = next(movie for movie in selected_theater.movies 
                                           if movie.title == selected_movie_title and movie.show_time == show_time_choice)
                    selected_movie.display_seats()

                    try:
                        num_tickets = int(input("Enter the number of tickets: "))
                        if num_tickets > 0:
                            print(f"Ticket Price: {selected_movie.price_per_ticket}")
                            total_cost = num_tickets * selected_movie.price_per_ticket
                            print(f"Total Cost: {total_cost}")

                            proceed = input("Proceed with booking? (y/n): ").lower()
                            if proceed == 'y':
                                booked_seats = []
                                for _ in range(num_tickets):
                                    while True:
                                        try:
                                            seat_number = int(input(f"Enter the seat number (1-{selected_movie.rows * selected_movie.cols}) for ticket {_+1}: "))
                                            if 1 <= seat_number <= selected_movie.rows * selected_movie.cols: 
                                                if selected_movie.book_seat(seat_number):
                                                    booked_seats.append(f"Seat {seat_number}")
                                                    break
                                                else:
                                                    print("Seat not available. Please select another seat.")
                                            else:
                                                print("Invalid seat number. Please enter a valid seat number.")
                                        except ValueError:
                                            print("Invalid input. Please enter a valid seat number.")

                                selected_movie.display_seats() 

                                print("\nBooking Successful!")
                                print(f"User Name: {user_name}")
                                print(f"Phone Number: {user_phone}")
                                print(f"Movie: {selected_movie.title}")
                                print(f"Show Time: {selected_movie.show_time}")
                                print(f"Theater: {selected_theater.name}")
                                print(f"Number of Tickets: {num_tickets}")
                                print(f"Booked Seats: {', '.join(booked_seats)}")
                                print(f"Total Cost: {total_cost}")
                            else:
                                print("Booking canceled.")
                    except ValueError:
                        print("Invalid input for number of tickets.")
                else:
                    print("Invalid theater selection.")
            else:
                print("Invalid movie selection.")

            # Prompt the user if they want to continue booking
            continue_booking = input("Do you want to book another ticket? (y/n): ").lower()
            if continue_booking != 'y':
                break 

if __name__ == "__main__":
    booking_system = BookingSystem()
    booking_system.user_login()
