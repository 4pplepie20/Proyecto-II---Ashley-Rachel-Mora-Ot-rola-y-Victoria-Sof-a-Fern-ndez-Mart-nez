import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame




# Ventana principal
ventana = tk.Tk()
ventana.title("Juego Proyecto II")
ventana.geometry("620x520")
ventana.resizable(False, False)
main_frame = tk.Frame(ventana, bg="#D12B4D")
main_frame.pack(fill=tk.BOTH, expand=True)

#Función para abrir botones
def click1():
  top = tk.Toplevel(ventana)
  top.title("Registro")
  top.geometry("420x280")

def click2(): #PARA ABRIR EL JUEGO
  top = tk.Toplevel(ventana)
  top.title("Juego")
  top.geometry("600x420")

def click3():
  top = tk.Toplevel(ventana)
  top.title("Puntaje")
  top.geometry("420x280")





# Botones ventana principal
Boton1= tk.Button(main_frame, text="Registro", command=click1, bg="#532B97",    fg="white",
activebackground="#C3D12B",
activeforeground="white",
font=("Arial", 12, "bold"),
width=24,height=2)
Boton1.pack(pady=22)

Boton2= tk.Button(main_frame, text="JUGAR", command=click2, bg="#532B97",    fg="white",
activebackground="#C3D12B",
activeforeground="white",
font=("Arial", 12, "bold"),
width=24,height=2)
Boton2.place(x=186,y=200)

Boton3= tk.Button(main_frame, text="Puntajes", command=click3, bg="#532B97",    fg="white",
activebackground="#C3D12B",
activeforeground="white",
font=("Arial", 12, "bold"),
width=24,height=2)
Boton3.place(x=186, y=400)


ventana.mainloop()