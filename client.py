import socket

def main():
    # Connect to the server, receive the city information,
    # prompt the user for a temperature prediction, and send it to the server.
    
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect(('localhost', 8888))
        print("Connected to the server on port 8888.")
        
        # Receive initial city information from server
        city_info = client_socket.recv(1024).decode()
        print(f"\nServer: {city_info}")
        
        while True:
            # Get user prediction
            prediction = input("Enter your temperature prediction (or type 'END' to quit): ").strip()
            
            # Check if user wants to quit
            if prediction.upper() == "END":
                client_socket.send("END".encode())
                
                # Get final message
                final_message = client_socket.recv(1024).decode()
                print(f"Server: {final_message}")
                break
            
            try:
                # Validate input is a number
                float(prediction)
                
                # Send prediction to server
                client_socket.send(prediction.encode())
                
                # Receive response from server
                server_response = client_socket.recv(1024).decode()
                print(f"Server: {server_response}")
                
                # Check if game round is over (correct guess or out of attempts)
                if "Correct!" in server_response or "Sorry, you've used all" in server_response:
                    # Ask if user wants to continue
                    continue_game = input("\nWould you like to play again? (yes/no): ").strip().lower()
                    
                    if continue_game != 'yes':
                        # Send END command to server
                        client_socket.send("END".encode())
                        
                        # Get final message
                        final_message = client_socket.recv(1024).decode()
                        print(f"Server: {final_message}")
                        break
                    else:
                        # Request new city
                        client_socket.send("NEW".encode())
                        
                        # Receive new city info
                        city_info = client_socket.recv(1024).decode()
                        print(f"\nServer: {city_info}")
            
            except ValueError:
                print("Please enter a valid number.")
                
    except ConnectionRefusedError:
        print("Could not connect to the server. Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == '__main__':
    main()