import serial
import tkinter as tk

# Configuration du port série
SERIAL_PORT = "COM4"  # Changez selon votre configuration
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
        style = f"S{size_var.get()}B{bold_var.get()}C{color_var.get()}"  # Ajout couleur
        ser.write((style + text + "\n").encode('utf-8'))

# Interface graphique Tkinter
root = tk.Tk()
root.title("Affichage Arduino")

tk.Label(root, text="Texte à envoyer :").pack()
entry = tk.Entry(root, width=40, font=("Arial", 14))
entry.pack(pady=5)
entry.bind("<KeyRelease>", send_text)  # Envoi du texte à chaque frappe

# Choix de la taille du texte
tk.Label(root, text="Taille du texte :").pack()
size_var = tk.IntVar(value=1)
size_scale = tk.Scale(root, from_=1, to=3, orient="horizontal", variable=size_var, command=lambda x: send_text())
size_scale.pack()

# Option de gras
bold_var = tk.IntVar(value=0)
bold_check = tk.Checkbutton(root, text="Gras", variable=bold_var, command=send_text)
bold_check.pack()

# Option de couleur
tk.Label(root, text="Couleur :").pack()
color_var = tk.IntVar(value=1)  # 1 = Blanc, 0 = Noir
color_white = tk.Radiobutton(root, text="Blanc", variable=color_var, value=1, command=send_text)
color_black = tk.Radiobutton(root, text="Noir", variable=color_var, value=0, command=send_text)
color_white.pack()
color_black.pack()

root.mainloop()

# Fermeture propre du port série
if ser:
    ser.close()
