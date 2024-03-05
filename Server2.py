import socket
import struct
import numpy as np
import cv2
import os

image_counter = 0  # Initialize a counter for image filenames

def receive_image(connection):
    global image_counter
    while True:
        # Receive file extension
        extension = connection.recv(1024).decode()
        if extension == "DONE":
            print("No more images to receive.")
            break
        if not extension:
            print("No extension received. Ending session.")
            break

        print("Received file type: ", extension)

        # Ensure we receive exactly 4 bytes for the size
        fhead = b''
        while len(fhead) < 4:
            packet = connection.recv(4 - len(fhead))
            if not packet:
                raise Exception("Connection closed prematurely")
            fhead += packet

        size, = struct.unpack("I", fhead)
        print(f"Expected image size: {size} bytes")

        # Receive the image data
        data = b''
        while len(data) < size:
            packet = connection.recv(1024)
            if not packet:
                break  # Connection might have been closed
            data += packet

        # Check if data received matches the expected size
        if len(data) < size:
            print("Received incomplete image data.") 
            continue  

        # Save the image data to a file 
        filename = f"received_image_{image_counter}.{extension}"
        image_counter += 1
        with open(filename, 'wb') as img_file:
            img_file.write(data)
        print(f"Image saved as {filename}")
        
       

def start_server():
    host = "0.0.0.0"  # Listen on all network interfaces
    port = 20001

    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind((host, port))
    serverSock.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = serverSock.accept()
        print(f"Connected by {addr}")
        conn = ssl.wrap_socket(conn, server_side=True, certfile="server.pem", keyfile="server.key", ssl_version=ssl.PROTOCOL_TLS)

        message = conn.recv(1024).decode()
        print(message)
        
        receive_image(conn)
        
        conn.close()
        print("Connection closed. Waiting for next client...")

if _name_ == "_main_":
    start_server()