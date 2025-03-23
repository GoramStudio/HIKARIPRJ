import serial
import tkinter as tk

# Configuration du port série (remplacez 'COM4' par votre port si nécessaire)
SERIAL_PORT = "COM4"
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException:
    print(f"Erreur : Impossible d'ouvrir le port {SERIAL_PORT}")
    ser = None

def send_text(event=None):
    """Envoie le texte entré par l'utilisateur au port série."""
    if ser:
        text = entry.get()
        ser.write((text + "\n").encode('utf-8'))

# Interface graphique Tkinter
root = tk.Tk()
root.title("Affichage Arduino")

entry = tk.Entry(root, width=40, font=("Arial", 14))
entry.pack(pady=10)
entry.bind("<KeyRelease>", send_text)  # Envoie du texte à chaque touche pressée

root.mainloop()

# Fermeture propre du port série
if ser:
    ser.close()
