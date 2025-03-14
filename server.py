import socket
import pandas as pd
import random

# Server Configuration
HOST = "localhost"
PORT = 8888

# Load weather data from the Excel file
df = pd.read_excel("weathers.xlsx")  # Make sure the file exists in the same directory

def handle_request(client_connection):
    """Processes the client's guess and provides feedback."""
    
    # Select a random city
    city, actual_temp = random.choice(df.values)
    client_connection.send(f"Predict the temperature for: {city}".encode())

    attempts = 0  # Incorrect guess counter

    while True:
        # Receive the guess from the client
        guess = client_connection.recv(1024).decode().strip()

        if guess.upper() == "END":
            print("Client terminated the connection.")
            client_connection.send("Connection closed.".encode())
            break

        try:
            guess_temp = int(guess)
        except ValueError:
            client_connection.send("Invalid input, please enter a number.".encode())
            continue

        # Check if the guess is within a 10% tolerance range
        tolerance = actual_temp * 0.1
        if abs(guess_temp - actual_temp) <= tolerance:
            client_connection.send(f"Congratulations! Correct guess: {actual_temp}°C".encode())
            break
        else:
            attempts += 1
            if attempts >= 3:
                client_connection.send(f"3 incorrect guesses! The correct temperature was: {actual_temp}°C".encode())
                break
            hint = "Higher" if guess_temp < actual_temp else "Lower"
            client_connection.send(f"Incorrect guess. {hint}".encode())

def serve_forever():
    """Starts the server and handles client connections."""
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    
    print(f"Server started, waiting for clients on port: {PORT}...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection established: {client_address}")
        
        handle_request(client_socket)

        print("Connection closed, waiting for a new client...")
        client_socket.close()

if __name__ == '__main__':
    serve_forever()
