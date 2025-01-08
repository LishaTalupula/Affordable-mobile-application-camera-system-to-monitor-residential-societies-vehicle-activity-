import tkinter as tk
from tkinter import messagebox, Label, Entry, Button
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import numpy as np
import imutils
import time
import requests
import cv2
import os
from tkinter import ttk

# Number plate detection variables
number_plate_list = ["MH02AJ344", "TN22DQ6016", "TN88F4089", "HR26DQ5551", "KA02MP9657"]
pname = 0
final_status = ''

# Function to handle login logic
def check_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "password":  # Dummy check for simplicity
        login_window.destroy()  # Close login window
        home_page()  # Open home page
    else:
        messagebox.showerror("Login Error", "Invalid Username or Password")

# Home page function after successful login
def home_page():
    global root
    root = tk.Tk()
    root.title("Residentialsecurity")
    root.geometry('1100x800')
    root.configure(background="lightgrey")

    message = tk.Label(root, text="FAST,EASY AND ACCURATE", bg="white", fg="black", width=48,
                       height=2, font=('times', 30, 'italic bold '))
    message.place(x=0, y=0)

    def get_plate_number():
        global pname
        regions = ['in']  # Change to your country
        with open('plate.jpg', 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),
                files=dict(upload=fp),
                headers={'Authorization': 'Token b565a03a76bac29d2d04a1ea279bd6f69b006de5'})
        try:
            plate_number = response.json()['results'][0]['plate']
            pname = plate_number.upper()
            print(pname)
        except:
            print("none")
            pass

    def close():
        sc1.destroy()

    def ok_screen():
        global sc1
        global final_status
        sc1 = tk.Tk()
        sc1.geometry('300x100')
        sc1.title('Status')
        sc1.configure(background='snow')
        Label(sc1, text=final_status, fg='red', bg='white', font=('times', 16, ' bold ')).pack()
        Button(sc1, text='OK', command=close, fg="black", bg="lawn green", width=9, height=1, 
               activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

    def get_vio():
        global pname
        global final_status
        if pname in number_plate_list:
            final_status = "Authorized"
        else:
            final_status = "Unauthorized"
        ok_screen()
        print(final_status)

    def clear():
        cv2.destroyAllWindows()
        rtitle.destroy()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    def analysis():
        global rtitle
        frame = cv2.imread(path)
        frame = imutils.resize(frame, width=400)
        cv2.imwrite("plate.jpg", frame)
        get_plate_number()
        rtitle = tk.Label(text=pname.upper(), background="snow", fg="Black", font=("", 15, 'bold'))
        rtitle.place(x=830, y=300)

        clrWindow = tk.Button(root, text="Clear", command=clear, fg="black", bg="lawn green", width=15, height=3, 
                              activebackground="Red", font=('times', 15, ' bold '))
        clrWindow.place(x=90, y=600)

        fineWindow = tk.Button(root, text="Submit", command=get_vio, fg="black", bg="lawn green", width=15, height=3, 
                               activebackground="Red", font=('times', 15, ' bold '))
        fineWindow.place(x=800, y=400)

    def openphoto():
        global path
        path = askopenfilename(filetypes=[("Image File", '.jpg')])
        frame = cv2.imread(path)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        cv2image = imutils.resize(cv2image, width=200)
        img = Image.fromarray(cv2image)
        tkimage = ImageTk.PhotoImage(img)
        myvar = tk.Label(root, image=tkimage, height="450", width="350")
        myvar.image = tkimage
        myvar.place(x=350, y=180)

        preImg = tk.Button(root, text="Predict", fg="black", command=analysis, bg="lawn green", width=15, height=3, 
                           activebackground="Red", font=('times', 15, ' bold '))
        preImg.place(x=90, y=450)

    def capture():
        global path
        cam = cv2.VideoCapture(0)
        time.sleep(0.5)
        ret, img = cam.read()
        captured = cv2.imwrite("./Captured_images/Captured.jpg", img)
        cam.release()
        path = "./Captured_images/Captured.jpg"
        frame = cv2.imread(path)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        cv2image = imutils.resize(cv2image, width=400)
        img = Image.fromarray(cv2image)
        tkimage = ImageTk.PhotoImage(img)
        myvar = tk.Label(root, image=tkimage, height="450", width="350")
        myvar.image = tkimage
        myvar.place(x=350, y=230)

        preImg = tk.Button(root, text="Predict", fg="black", command=analysis, bg="lawn green", width=15, height=3, 
                           activebackground="Red", font=('times', 15, ' bold '))
        preImg.place(x=90, y=450)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    button1 = tk.Button(root, text="Select Photo", command=openphoto, fg="white", bg="blue2", width=15, height=3, 
                        activebackground="Red", font=('times', 15, ' bold '))
    button1.place(x=90, y=150)

    capbut = tk.Button(root, text="Capture", fg="black", command=capture, bg="lawn green", width=15, height=3, 
                       activebackground="Red", font=('times', 15, ' bold '))
    capbut.place(x=90, y=300)

    quitWindow = tk.Button(root, text="Quit", command=on_closing, fg="white", bg="Red", width=15, height=3, 
                           activebackground="Red", font=('times', 15, ' bold '))
    quitWindow.place(x=800, y=530)

    root.mainloop()

# Login page function
# Login page function
from tkinter import Tk, Label
from PIL import Image, ImageTk

def create_mixed_gradient(width, height, color1, color2):
    """ Create a horizontal gradient from color1 to color2. """
    gradient = Image.new('RGB', (width, height))
    
    # Loop through each pixel in the width and calculate the gradient color
    for i in range(width):
        ratio = i / width  # Calculate the ratio based on horizontal position
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        # Apply the gradient to all pixels in the current column
        for j in range(height):
            gradient.putpixel((i, j), (r, g, b))
    
    return gradient

# Initialize window
login_window = Tk()
login_window.title("Residentialsecurity")
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()

# Set window size to full screen
login_window.geometry(f"{screen_width}x{screen_height}")

# Define two colors to mix (e.g., Red and Yellow)
color1 = (120, 81, 169)  # Red color
color2 = (211, 211, 211)  # Yellow color

# Create the gradient image (mixed colors horizontally)
gradient_image = create_mixed_gradient(screen_width, screen_height, color1, color2)

# Convert the gradient image to Tkinter PhotoImage format
gradient_image_tk = ImageTk.PhotoImage(gradient_image)

# Add the gradient image to a label as the background
bg_label = Label(login_window, image=gradient_image_tk)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

title_label = tk.Label(login_window, text="WELCOME TO THE RESIDENTIAL SECURITY", font=('times', 18,'italic bold' ))
title_label.pack(pady=20, anchor='center')

label_username = tk.Label(login_window, text="Username", font=('Arial', 14))
label_username.pack(pady=10)

username_entry = tk.Entry(login_window, font=('Arial', 14))
username_entry.pack(pady=10)

label_password = tk.Label(login_window, text="Password", font=('Arial', 14))
label_password.pack(pady=10)

password_entry = tk.Entry(login_window, font=('Arial', 14), show="*")
password_entry.pack(pady=10)

login_button = tk.Button(login_window, text="Login", width=20, height=2, bg="blue", fg="white", command=check_login)
login_button.pack(pady=20)
login_window.mainloop()




# Run the login page first
login_page()
