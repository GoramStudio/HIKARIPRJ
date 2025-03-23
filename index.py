import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import serial
import time
import cv2
import numpy as np

def send_data(image_path, text):
    ser = serial.Serial('COM4', 115200)
    time.sleep(2)
    
    # Process image
    img = Image.open(image_path).convert('L')
    img = img.resize((64, 64), Image.ANTIALIAS)
    img = img.point(lambda p: 255 if p > 128 else 0, '1')
    img_data = np.array(img, dtype=np.uint8)
    
    # Send image
    for y in range(0, 64, 8):
        for x in range(0, 64, 8):
            block = img_data[y:y+8, x:x+8]
            block_bytes = [int("".join(str(1-int(bit)) for bit in row), 2) for row in block]
            ser.write(bytearray([x, y]))
            ser.write(bytearray(block_bytes))
            time.sleep(0.005)
    
    # Send text
    ser.write(b'TEXT:' + text.encode('utf-8') + b'\n')
    ser.close()

def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((100, 100))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk
        img_label.file_path = file_path

def send():
    text = text_entry.get()
    image_path = getattr(img_label, 'file_path', None)
    if image_path and text:
        send_data(image_path, text)

# GUI
root = tk.Tk()
root.title("Image & Text Sender")

tk.Button(root, text="Select Image", command=select_image).pack()
img_label = tk.Label(root)
img_label.pack()
text_entry = tk.Entry(root)
text_entry.pack()
tk.Button(root, text="Send", command=send).pack()

root.mainloop()
