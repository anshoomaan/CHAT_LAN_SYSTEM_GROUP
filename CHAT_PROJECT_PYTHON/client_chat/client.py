import socket
import os
import json  # To handle JSON serialization and deserialization

# Server configuration
HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server Port

#--------------------------------------------------------------------------------------------------------------

# Main client logic
#requested_func_number
def request_data(client_function_name, reciever=None, sender=None, inputed_text=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("[*] Connected to the server.")

    try:
        input_list = [client_function_name, reciever, sender, inputed_text]
        
        # sending the function no.
        print(f"Sending to server: {input_list}")

        # Send the list to the server
        client_socket.send(json.dumps(input_list).encode())

        # Receive and print the server's response
        server_response = client_socket.recv(1024).decode()
        server_result = json.loads(server_response)  # Decode JSON data into a Python list
        print(f"Received from server: {server_result}")
        return server_result
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("[!] Disconnected from server.")
        
#--------------------------------------------------------------------------------------------------------------

# function to be run on the client side
# def user_list():                                                    buttons all users
# file_data(reciever, sender, message):                               get content from specific file and update also
# def credentials(username,password):                                                  credential checker

#--------------------------------------------------------------------------------------------------------------

# request server for users
def user_list():
    result = request_data('user_list') # requested_func_number
    return result
# user_list()

#--------------------------------------------------------------------------------------------------------------

def file_data(reciever, sender, message):
    result = request_data('file_data',reciever, sender, message)
    return result
# file_data('a', 'mannu', '')

#--------------------------------------------------------------------------------------------------------------

def credentials(username, password, status):
    result = request_data('credentials',username, password, status)
    if result == True:
        writer_god(username)
        return True
    else:
        return False
# credentials('a', '1', 'login')
# credentials('mannu', '1', 'signup')

#--------------------------------------------------------------------------------------------------------------

# Get the current working directory
current_directory = os.getcwd()
print("Current working directory:", current_directory)
god_path = current_directory+'\\zgod_user.txt'

# god_path = r"C:\Users\ansho\OneDrive\Desktop\client_chat\zgod_user.txt"

def get_god_user():
    try:
        with open(god_path, 'r') as file:
            god_user = file.readline()
    except FileNotFoundError:
        print("error 1 ")
    except Exception as e:
        print("error 2 ")
    return god_user

#--------------------------------------------------------------------------------------------------------------

def writer_god(username):
    try:
        with open(god_path, 'w') as file:
            file.write(username)
    except FileNotFoundError:
        print("error 1 ")
    except Exception as e:
        print("error 2 ")
    return True

#--------------------------------------------------------------------------------------------------------------
