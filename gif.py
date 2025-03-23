import serial
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Configuration du port série (remplacez 'COM4' par votre port si nécessaire)
SERIAL_PORT = "COM4"
BAUD_RATE = 9600

# Ouverture du port série
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException:
    print(f"Erreur : Impossible d'ouvrir le port {SERIAL_PORT}")
    ser = None

def send_gif():
    """Sélectionne un GIF, le lit et envoie une seule frame à l'Arduino."""
    if ser:
        # Ouvre une fenêtre pour choisir le fichier GIF
        filepath = filedialog.askopenfilename(filetypes=[("Fichiers GIF", "*.gif")])
        if not filepath:
            return
        
        # Ouvre le fichier GIF
        gif = Image.open(filepath)
        
        # On prend la première frame du GIF pour tester
        frame = gif.convert("1")  # Convertir en noir et blanc (mode binaire)
        frame = frame.resize((128, 64))  # Redimensionner pour correspondre à l'écran
        
        pixels = frame.load()  # Charger les pixels de l'image
        
        # Envoi de chaque ligne de pixels de l'image
        for y in range(64):  # Parcours chaque ligne de l'image
            line_data = []
            for x in range(0, 128, 8):  # Parcours chaque colonne de 8 pixels
                byte = 0
                for bit in range(8):
                    pixel_value = 255 if pixels[x + bit, y] == 255 else 0  # Blanc=255, Noir=0
                    byte |= (pixel_value << (7 - bit))  # Décalage des bits pour former un octet
                line_data.append(byte)  # Ajouter l'octet à la ligne
                
            # Envoie de chaque ligne de 16 octets à l'Arduino
            for byte in line_data:
                ser.write(bytes([byte]))  # Envoi de l'octet
            time.sleep(0.005)  # Petit délai pour assurer que l'Arduino peut traiter la donnée
            
        ser.write(b'\n')  # Fin de la frame
        
        print("Une seule frame envoyée à l'Arduino.")

# Interface graphique Tkinter
root = tk.Tk()
root.title("Envoyer un GIF à l'Arduino")

send_button = tk.Button(root, text="Envoyer un GIF", font=("Arial", 14), command=send_gif)
send_button.pack(pady=20)

root.mainloop()

# Fermeture propre du port série
if ser:
    ser.close()
