import socket
import threading
import random
import os
import sys
import json  # To handle JSON serialization and deserialization

# Server configuration
HOST = '127.0.0.1'  # localhost
PORT = 65432        # Arbitrary non-privileged port
MAX_CLIENTS = 10    # Maximum number of clients

# Get the current working directory
current_directory = os.getcwd()
# print("Current working directory:", current_directory)
folder_path = current_directory+"\\FILESYSTEM_DATA"

#--------------------------------------------------------------------------------------------------------------

def user_list():
    try:
        list = []
        with open(folder_path+'\\CREDENTIALS\\user_pass.txt', 'r') as file:
            lines = file.readlines()
            for i in lines:
                word = ''
                for j in i:
                    if "_" in j:
                        list.append(word)
                        break
                    else:
                        word = word+j
        # print(list)
        return list
    except FileNotFoundError:
        print("error this 1 ")
    except Exception as e:
        print("error this 2 ")
# user_list()

#--------------------------------------------------------------------------------------------------------------

def credentials(username, password, status):
    try:
        with open(folder_path+'\\CREDENTIALS\\user_pass.txt', 'r') as file:
            lines = file.readlines()
            if status == "login":
                for i in lines:
                    if i == username+"_"+password+"\n":
                        print(i ,"true")
                        return True
                print("false 1")
                return False    
            
            elif status == "signup":
                check = False
                for i in lines:
                    if i == username+"_"+password+"\n":
                        check = True
                # adding user
                if check == False:
                    try:
                        with open(folder_path+'\\CREDENTIALS\\user_pass.txt', 'a') as file:
                            file.write(username+"_"+password+"\n")
                    except FileNotFoundError:
                        print("error 1 ")
                    except Exception as e:
                        print("error 2 ")
                    print(username+"_"+password,"true")
                    return True
                else:
                    print("check was true")
                    return False
                
            else:
                print("status is wronge")
                
    except FileNotFoundError:
        print("error this1 ")
    except Exception as e:
        print("error this 2 ")
        
# credentials('mannu', '123', 'signup')
# credentials('a', '123', 'signup')
# credentials('mannu', '123', 'signup')
# credentials('divya', '123', 'signup')
# credentials('ishika', '123', 'signup')

#--------------------------------------------------------------------------------------------------------------

def file_data(reciever, sender, message):
    file_name1 = reciever+sender
    file_name2 = sender+reciever
    filename = ''
    
    print(" inside of a big function ",reciever, sender, message)

    for root, dirs, files in os.walk(folder_path):
        if file_name1 in files:
            print ( " error code for this stupid func is 1" )
            file_path = os.path.join(root, file_name1)
            print(f"File found 1: {file_path}")
            filename = file_name1
            break
        
        elif file_name2 in files:
            print ( " error code for this stupid func is 2" )
            file_path = os.path.join(root, file_name2)
            print(f"File found 2: {file_path}")
            filename = file_name2
            break
        
        else:
            print ( " error code for this stupid func is 3" , folder_path+'\\'+filename)
            with open(folder_path+'\\'+file_name1, 'w') as file:
                file.write("")  # Create an empty file         
            print("File not found. file created with name :",file_name1)
            filename = file_name1
            break
    
    # Search for the file in the folder
    if message == '':
        print ( " error code for this stupid func is 4" )
        try:
            with open(folder_path+'\\'+filename, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print("error 1 ")
        except Exception as e:
            print("error 2 ")
            
    else:
        print ( " error code for this stupid func is 5" )
        try:
            with open(folder_path+'\\'+filename, 'a') as file:
                file.write(sender+"@$#: "+message+"\n")
            with open(folder_path+'\\'+filename, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print("error 3 ")
        except Exception as e:
            print("error 4 ")
            
#--------------------------------------------------------------------------------------------------------------

# Function to handle client connection
def handle_client(client_socket, client_address):
    print(f"[+] Connection from {client_address}")
    try:
        # Receive data from the client in format (client_function_name, reciever=None, sender=None, inputed_text=None)
        data = client_socket.recv(1024).decode()
        client_input = json.loads(data)  # Decode JSON data into a Python list
        print(f"Received input data from client :  {client_address}: {client_input}")

        if(client_input[0]=='user_list'):
            result = user_list()
            
        elif(client_input[0]=='file_data'):
            reciever = client_input[1]
            sender = client_input[2]
            message = client_input[3]
            result = file_data(reciever, sender, message)
            
        elif(client_input[0]=='credentials'):
            username = client_input[1]
            password = client_input[2]
            status = client_input[3]
            result = credentials(username, password, status)
        
        else:
            print("SOMETHING WENT WRONGE")
            
        # Send the result back to the client
        print(f"Sending to {client_address}: {result}")
        client_socket.send(json.dumps(result).encode())
        
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"[-] Connection with {client_address} closed")
   
#--------------------------------------------------------------------------------------------------------------

# Main server logic
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            # Start a new thread for each client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down.")
            server_socket.close()
            break

if __name__ == "__main__":
    main()

#--------------------------------------------------------------------------------------------------------------
