import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame

# Variable global que revisa si una ventana secundaria que está abierta
ventana_actual = None



# Cuando el usuario cierra una ventana secundaria desde la "X"
def cerrar_root():
    global ventana_actual
    if ventana_actual is not None and ventana_actual.winfo_exists():
        ventana_actual.destroy()
        ventana.deiconify() # Se vuelve a hacer visible el menú principal

#Función de la ventana principal para salir por completo del juego
def salir_del_juego():
   ventana.destroy()


# Ventana principal
ventana = tk.Tk()
ventana.title("Juego Proyecto II")
ventana.geometry("620x520")
ventana.resizable(False, False)
main_frame = tk.Frame(ventana, bg="#D12B4D")
main_frame.pack(fill=tk.BOTH, expand=True)

#Función para abrir botones
def click1():
  global ventana_actual
  ventana.withdraw() #Oculta el menú principal
  top = tk.Toplevel(ventana)
  top.title("Registro")
  top.geometry("420x280")
  ventana_actual = top
#Boton de X en registro 
  boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), 
                              bg="#532B97", fg="white", command=cerrar_root)
  boton_cerrado.place(x=385, y=5)
  top.protocol("WM_DELETE_WINDOW", cerrar_root)


def click2(): 
  global ventana_actual
  ventana.withdraw()
  top = tk.Toplevel(ventana)
  top.title("Juego")
  top.geometry("600x420")
  ventana_actual = top
  #Boton de X en Juego
  boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), 
                              bg="#532B97", fg="white", command=cerrar_root)
  boton_cerrado.place(x=565, y=5)
  top.protocol("WM_DELETE_WINDOW", cerrar_root)

def click3():
  global ventana_actual
  ventana.withdraw()
  top = tk.Toplevel(ventana)
  top.title("Puntaje")
  top.geometry("420x280")
  ventana_actual = top
#Boton de X en Puntajes
  boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), 
                              bg="#532B97", fg="white", command=cerrar_root)
  boton_cerrado.place(x=385, y=5)
  top.protocol("WM_DELETE_WINDOW", cerrar_root)





# Botones ventana principal 

boton_cerrar_principal = tk.Button(main_frame, text='X', font=("Arial", 10, "bold"), 
                                   bg="#532B97", fg="white", command=salir_del_juego)
boton_cerrar_principal.place(x=585, y=5) 

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

#BOTÓN MUSICA
pygame.mixer.init()
def alternar_musica():
    global musica_activa
    
    if not musica_activa:
        pygame.mixer.music.load("mi_cancion.mp3")
        pygame.mixer.music.play(-1)
        Boton4.config(text="Pausar Música")
        musica_activa = True
    else:
        pygame.mixer.music.stop()
        Boton4.config(text="Reproducir Música")
        musica_activa = False

Boton4 = tk.Button(main_frame, text="ON/OFF MUSICA", command=alternar_musica, bg="#532B97", fg="white")
Boton4.place (x=260, y= 460)  

musica_activa = False

ventana.mainloop()