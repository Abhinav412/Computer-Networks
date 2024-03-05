import socket
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import struct
import os

def connect_server():
    global clientSock
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSock.connect(("10.1.21.112", 20001))
    clientSock.send("Client connection established".encode())

def upload(clientSock):
    filepaths = filedialog.askopenfilenames(filetypes=[("image", ".jpeg"), ("image", ".png"), ("image", ".jpg")])
    for filepath in filepaths:
        if not filepath:
            continue

        print("File location: " + filepath)
        _, extension = os.path.splitext(filepath)
        extension = extension.lstrip('.')
        print("File Type: " + extension)

        clientSock.send(extension.encode())

        img = cv2.imread(filepath)
        img_encode = cv2.imencode("." + extension, img)[1]
        data = img_encode.tobytes()

        print(f"Length of Data: {len(data)}")

        fhead = struct.pack("I", len(data))
        clientSock.send(fhead)

        for i in range(0, len(data), 1024):
            clientSock.send(data[i:i + 1024])

        print("Image sent:", os.path.basename(filepath))
    
    clientSock.send("DONE".encode())

def submit_login():
    username = username_value.get()
    password = password_value.get()
    if username == "client" and password == "client":
        print("You are now logged in")
        window.destroy()
        connect_server()
        upload_file = tk.Tk()
        upload_file.geometry("400x300")
        upload_file.title("Upload an Image")
        tk.Label(upload_file, text="Upload an Image", font="times 15 bold").grid(row=3, column=3)
        tk.Button(upload_file, text="Upload an Image", command=lambda: upload(clientSock)).grid(row=4, column=4)
    else:
        print("Error")

window = tk.Tk()
window.geometry("250x200")
window.title("Client Login")

username_value = tk.StringVar()
password_value = tk.StringVar()

tk.Label(window, text="Client Login", font="times 15 bold").grid(row=0, column=3)
tk.Label(window, text="Username").grid(row=1, column=2, padx=10, pady=10)
tk.Label(window, text="Password").grid(row=2, column=2, padx=10)
username_box = tk.Entry(window,textvariable=username_value).grid(row=1, column=3)
password_box = tk.Entry(window,textvariable=password_value, show="*").grid(row=2, column=3)
tk.Button(window, text="Login", command=submit_login).grid(row=4, column=3, pady=20)

window.mainloop()