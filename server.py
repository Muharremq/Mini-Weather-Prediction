import socket
import random
import pandas as pd

def handle_client_session(client_connection):
    global weather_data
    
    try:
        while True:
            # Select a random city
            current_city = random.choice(weather_data['City'].tolist())
            actual_temp = float(weather_data.loc[weather_data['City'] == current_city, 'Temp'].values[0])
            
            # Send city name to client
            city_info = f"Predict the temperature for {current_city}"
            client_connection.send(city_info.encode())
            
            # Track number of guesses
            incorrect_guesses = 0
            max_attempts = 3
            
            while incorrect_guesses < max_attempts:
                # Receive guess from client
                client_data = client_connection.recv(1024).decode().strip()
                
                # Check if client wants to end connection
                if client_data.upper() == "END":
                    client_connection.send("Connection terminated.".encode())
                    return False  # Signal to close connection
                
                # Check if client is requesting a new city
                if client_data.upper() == "NEW":
                    break  # Break inner loop to get a new city
                
                try:
                    # Convert guess to float
                    guess = float(client_data)
                    
                    # Calculate tolerance range (10% of actual temperature)
                    tolerance = actual_temp * 0.1
                    lower_bound = actual_temp - tolerance
                    upper_bound = actual_temp + tolerance
                    
                    # Check if guess is within tolerance
                    if lower_bound <= guess <= upper_bound:
                        success_message = f"Correct! The temperature in {current_city} is {actual_temp}°C."
                        client_connection.send(success_message.encode())
                        break  # Break inner loop to get confirmation for new city
                    else:
                        incorrect_guesses += 1
                        
                        # Provide hint
                        if guess < actual_temp:
                            hint = "Higher"
                        else:
                            hint = "Lower"
                        
                        # Check if this was the last attempt
                        if incorrect_guesses >= max_attempts:
                            final_message = f"Sorry, you've used all {max_attempts} attempts. The temperature in {current_city} is {actual_temp}°C."
                            client_connection.send(final_message.encode())
                            break  # Break inner loop to get confirmation for new city
                        else:
                            attempts_left = max_attempts - incorrect_guesses
                            hint_message = f"{hint}. {attempts_left} attempts remaining."
                            client_connection.send(hint_message.encode())
                            
                except ValueError:
                    error_message = "Please enter a valid number."
                    client_connection.send(error_message.encode())
            
            # After inner loop breaks, wait for client's next command (will be either NEW or END)
            # This is handled at the beginning of the outer loop
            
    except Exception as e:
        print(f"Error in client session: {e}")
        return False

def serve_forever():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reusing the same address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to localhost and port 8888
    server_socket.bind(('localhost', 8888))
    
    # Listen for incoming connections
    server_socket.listen(1)
    print("Server started. Listening on port 8888...")
    
    try:
        while True:
            # Accept client connection
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from {client_address}")
            
            try:
                # Handle client session
                handle_client_session(client_socket)
            except Exception as e:
                print(f"Error handling client: {e}")
            finally:
                client_socket.close()
                print(f"Connection with {client_address} closed.")
                
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == '__main__':
    # Load weather data
    try:
        # Try to load the Excel file
        weather_data = pd.read_excel('weathers.xlsx')
        print("Weather data loaded successfully.")
        print(weather_data)
    except Exception as e:
        # If Excel file can't be loaded, create the data manually from the image
        print(f"Could not load Excel file: {e}")
        print("Creating weather data manually...")
        weather_data = pd.DataFrame({
            'City': ['New York', 'Madrid', 'Chicago', 'Athens', 'Miami', 
                     'London', 'Berlin', 'Tokyo', 'Sydney', 'Toronto'],
            'Temp': [15, 22, 10, 28, 30, 12, 18, 20, 25, 14]
        })
    
    # Start the server
    serve_forever()