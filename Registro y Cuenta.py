import json

"DATOS DE USUARIO"
class Usuario: #Clase encargada de obtener todos los datos necesarios de una cuenta de usuario

    'Atributos'
    def __init__(self, usuario, contrasena, victorias_atacante = 0, victorias_defensor = 0): #Los datos a guardas. El self es solo para llamar al atributo como parte de la clase y la función def __init__ sirve para crear atributos
        self.usuario = usuario #Nombre de usuario
        self.contrasena = contrasena #Contraseña
        self.victorias_atacante = victorias_atacante #Cantidad actual de victorias como atacante
        self.victorias_defensor = victorias_defensor #Cantidad actual de victorias como defensor

    'Métodos'
    def obtener_nombre(self): #Obtiene nombre de usuario
        return self.usuario #El return hace que se muestre el dato
    
    def obtener_contrasena(self): #Obtiene contraseña
        return self.contrasena
    
    def obtener_victorias_atacante(self): #Obtiene la cantidad de victorias actuales como atacante
        return self.victorias_atacante 
    
    def obtener_victorias_defensor(self): #Obtiene la cantidad de victorias actuales como atacante
        return self.victorias_defensor
    
    def nueva_victoria_atacante(self): #Suma una victoria si el usuario cumple la condición de victoria como atacante
        self.victorias_atacante += 1 #Suma 1 la nueva victoria
    
    def nueva_victoria_defensor(self): #Suma una victoria si el usuario cumple la condición de victoria como defensor
        self.victorias_defensor += 1
    
"GESTIONADOR DE TODOS LOS USUARIOS Y GUARDADO"
class RegistroUsuarios: #Encargada de registrar todos los usuarios y guardar sus datos

    'Atributos'
    def __init__(self):
        self.lista_usuarios = [] #Guarda a todos los usuarios en una lista de listas
        self.archivo = "usuario.json" #Obtiene los datos guardados de los usuarios
        self.cargar_usuarios() #LLamada a una función que sirve para cargar los datos guardados de todos los usuarios

    'Métodos'
    def cargar_usuarios(self): #Función que sirve para buscar a un usuario en específico dentro de los archivos guardados
        try: #El try es para buscar
            archivo = open(self.archivo, "r") #Sirve para abrir los archivos guardados
            datos = json.load(archivo) #el .load sirve para leer el archivo JSON e interpretarlo a un tipo de dato entendible 
            archivo.close() #Función para cerrar el archivo

            for fila in datos: #El for es utilizado para recorrer la lista con información de los usuarios
                usuario = Usuario(
                    fila[0], #Nombre de usuario en la posición 0
                    fila[1], #Contraseña en posición 1
                    fila[2], #Victorias como atacante en posición 2
                    fila[3] #Victorias como defensor en posición 3
                )

                self.lista_usuarios.append(usuario) #El .append concatena los usuarios en una matriz
        except: #Significa que si no hay ningún usuario registrado, entonces se devuelve una lista vacía
            self.lista_usuarios = [] #Muestra lista vacía sin usuarios

    def guardar_usuarios(self): #Función que guarda los datos de los usuarios
        datos = [] #Lista vacía para poder agregar nuevos datos

        for usuario in self.lista_usuarios: #recorre la lista
            fila = [
                usuario.obtener_nombre(), #Nombre obtenido desde la clase Usuario
                usuario.obtener_contrasena(), #Contraseña obtenida desde la clase Usuario
                usuario.obtener_victorias_atacante(), #Victorias actuales como defensor obtenidas desde la clase Usuario
                usuario.obtener_victorias_defensor() #Victorias actuales como defensor obtenidas desde la clase Usuario
            ]

            datos.append(fila) #Concatenación de datos

        archivo = open(self.archivo, "w") #Abre el archivo y se escribe dentro de él
        json.dump(datos, archivo) #El json.dump sirve para convertir datos de Python a datos de formato JSON

        archivo.close() #Cierra el archivo

    def crear_usuario(self, nombre, contrasena): #Función para condiciones de crear nuevos usuarios
        for usuario in self.lista_usuarios: #Recorre la lista
            if usuario.obtener_nombre() == nombre:
                return False
            
        nuevo = Usuario(nombre, contrasena) #Se crea nuevo usuario
        self.lista_usuarios.append(nuevo) #Se concatena la información 
        self.guardar_usuarios() #Se llama a la función guardar_usuarios para guardar el nuevo usuario

        return True 


    def iniciar_sesion(self, nombre, contrasena):
        for usuario in self.lista_usuarios:
            if usuario.obtener_nombre() == nombre:
                if usuario.obtener_contrasena() == contrasena:
                    return usuario
        return None