import socket

# Server Connection Information
HOST = "localhost"
PORT = 8888

def main():
    """It connects to the server, gets predictions and displays the results."""
    
    # Create connection to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Get city information from server
    message = client.recv(1024).decode()
    print(message)

    while True:
        # Get predictions from user
        guess = input("Enter your temperature estimate (or exit by typing 'END'):")

        # If the user wants to exit
        if guess.upper() == "END":
            client.send(guess.encode())
            print("The connection was closed.")
            break

        # Send prediction to server
        client.send(guess.encode())

        # Get feedback from server
        response = client.recv(1024).decode()
        print(response)

        # If you guessed correctly or if you have 3 chances, you will exit.
        if "Correct guess" in response or "Your 3 guesses are over." in response:
            break

    client.close()

if __name__ == "__main__":
    main()
