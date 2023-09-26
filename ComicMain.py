import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
import time
from pathlib import Path
import os

tipo = None
comic = None
contents = None
formato = None

def pas():
    pass




class archivo:
    # Crea el objeto y guarda el contenido
    # E: nombre del archivo
    def __init__(self, nombre):
        self.nombre = nombre

        file = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\" + self.nombre, "r")
        text = file.read()
        self.contenido = text
        file.close()


    # Updatea el contenido del objeto
    def update(self):
        file = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\" + self.nombre, "r")
        text = file.read()
        self.contenido = text
        file.close()


    # Encripta el contenido del archivo
    def encriptar(self):
        filekey = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\filekey.key", "rb")
        key = filekey.read()
        fernet = Fernet(key)
        filekey.close()

        file = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\" + self.nombre, "rb")
        original = file.read()
        encriptado = fernet.encrypt(original)
        file.close()

        fileEncriptado = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\" + self.nombre, "wb")
        fileEncriptado.write(encriptado)
        fileEncriptado.close()

        self.update()


    # Desencripta el contenido del archivo
    def desencriptar(self):
        filekey = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\filekey.key", "rb")
        key = filekey.read()
        fernet = Fernet(key)
        filekey.close()

        fileEncriptado = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\" + self.nombre, "rb")
        encriptado = fileEncriptado.read()
        fileEncriptado.close()

        desencriptado = fernet.decrypt(encriptado)
        file = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\" + self.nombre, "wb")
        file.write(desencriptado)
        file.close()

        self.update()


    # Escribe el contenido en el archivo
    def escribir(self):
        file = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\" + self.nombre, "w")
        file.write(self.contenido)
        file.close()





class comicFile:
    # Crea el objeto y guarda el contenido
    # E: nombre del archivo
    def __init__(self, nombre):
            self.nombre = nombre

            file = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\comics\\" + self.nombre + ".txt", "r")
            text = file.read()
            self.contenido = text
            file.close()


    # Updatea el contenido del objeto
    def update(self):
        file = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\comics\\" + self.nombre + ".txt", "r")
        text = file.read()
        self.contenido = text
        file.close()


    # Escribe el contenido en el archivo
    def escribir(self):
        file = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\comics\\" + self.nombre + ".txt", "w")
        file.write(self.contenido)
        file.close()





# TKINTER -------------------------------------------------------------------------------------------------------------------------------------------------------
class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Comic Universe")
        self.geometry("800x900")

        # Fonts
        self.myFont1 = tkfont.Font(family='Neo Sans', size=40, weight="bold", slant="italic")
        self.myFont2 = tkfont.Font(family='Neo Sans', size=15)
        self.myFont3 = tkfont.Font(family='Bahnschrift', size=12)
        self.myFont4 = tkfont.Font(family='Bahnschrift', size=10)
        self.myFont5 = tkfont.Font(family='Bahnschrift', size=30)
        self.myFont6 = tkfont.Font(family='Bahnschrift', size=20, slant="italic")
        self.myFont7 = tkfont.Font(family='Bahnschrift', size=20)
        self.myFont8 = tkfont.Font(family='Bahnschrift', size=9)
        self.myFont9 = tkfont.Font(family='Segoe UI Emoji', size=30)
        self.myFont10 = tkfont.Font(family='Bahnschrift', size=15)


        # Genera un frame que va a tener todas las ventanas
        contenedor = tk.Frame(self)
        contenedor.pack(side="top", fill="both", expand=True)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (Inicio, Admin, Menu, MenuLeer, Lector, MenuTweak, MenuCrear, MenuEditar):
            page_name = F.__name__
            frame = F(parent = contenedor, controller = self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("Inicio")


    # Muestra la ventana que se le pida
    # E: nombre de la ventana
    def showFrame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


    # Abre una nueva ventana
    def abrirPersonajes(self):
        self.personajes = tk.Toplevel(self)

        self.personajes.title("Comic Universe: Personajes")

        self.personajes.geometry("700x700")

        self.personajes.configure(bg="#121212")

        labelTitulo = tk.Label(self.personajes, text="Personajes ", font=self.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        self.selPersonaje = ttk.Combobox(self.personajes, state="readonly", width=30, font=self.myFont3, values=self.getPersonajes())
        self.selPersonaje.place(relx = 0.5, anchor="center", y=120)
        self.selPersonaje.bind("<<ComboboxSelected>>", lambda x: self.showInfo(x))

        btnEditar = tk.Button(self.personajes, text="Editar", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.abrirEditor())
        btnEditar.place(relx = 0.95, anchor="center", y=60)

        btnUpdate = tk.Button(self.personajes, text="Update", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.updatePersonajes())
        btnUpdate.place(relx = 0.95, anchor="center", y=20)


    # Obtiene los personajes
    # S: lista con los nombres de los personajes
    def getPersonajes(self):
        res = []
        listaPerso = archivo("personajes.txt").contenido
        listaPerso = eval(listaPerso)
        for personaje in listaPerso:
            res.append(personaje["nombre"])
        return res


    # Enseña la informacion del personaje
    def showInfo(self, event=None):
        nombre = self.selPersonaje.get()
        lista = archivo("personajes.txt").contenido
        lista = eval(lista)

        for personaje in lista:
            if personaje["nombre"] == nombre:
                edad = personaje["edad"]
                cumple = personaje["cumple"]
                origen = personaje["lugar de origen"]
                afiliaciones = personaje["afiliaciones"]
                poderes = personaje["habilidades"]
                historia = personaje["historia"]
                aliados = personaje["aliados"]
                enemigos = personaje["enemigos"]
                break

        try:
            self.frameInfo
            self.frameInfo.destroy()
        except:
            pass

        # Informacion de los personajes
        self.frameInfo = tk.Frame(self.personajes, bg="#1f1f1f", width=610, height=530)
        self.frameInfo.place(relx=0.5, rely=0.58, anchor="center")
        self.frameInfo.grid_propagate(False)

        lblNombre = tk.Label(self.frameInfo, text="Nombre: ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblNombre.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        lblEdad = tk.Label(self.frameInfo, text="Edad: ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblEdad.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        lblCumple = tk.Label(self.frameInfo, text="Cumple: ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblCumple.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        lblOrigen= tk.Label(self.frameInfo, text="Origen: ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblOrigen.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        lblAfiliaciones = tk.Label(self.frameInfo, text="Afiliaciones: ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblAfiliaciones.grid(row=5, column=0, padx=20, pady=10, sticky="w")

        lblPoderes = tk.Label(self.frameInfo, text="Poderes: ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblPoderes.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        lblHistoria = tk.Label(self.frameInfo, text="Historia: ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblHistoria.grid(row=7, column=0, padx=20, pady=10, sticky="w")

        lblAliados = tk.Label(self.frameInfo, text="Aliados: ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblAliados.grid(row=8, column=0, padx=20, pady=10, sticky="w")

        lblEnemigos = tk.Label(self.frameInfo, text="Enemigos: ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblEnemigos.grid(row=9, column=0, padx=20, pady=10, sticky="w")

        tk.Label(self.frameInfo, text=nombre, font=self.myFont8, bg="#1f1f1f", fg="#FFFFFF", wraplength=400, justify="left").grid(row=1, column=1, padx=20, pady=10, sticky="w")
        tk.Label(self.frameInfo, text=edad, font=self.myFont8, bg="#1f1f1f", fg="#FFFFFF", wraplength=400, justify="left").grid(row=2, column=1, padx=20, pady=10, sticky="w")
        tk.Label(self.frameInfo, text=cumple, font=self.myFont8, bg="#1f1f1f", fg="#FFFFFF", wraplength=400, justify="left").grid(row=3, column=1, padx=20, pady=10, sticky="w")
        tk.Label(self.frameInfo, text=origen, font=self.myFont8, bg="#1f1f1f", fg="#FFFFFF", wraplength=400, justify="left").grid(row=4, column=1, padx=20, pady=10, sticky="w")
        tk.Label(self.frameInfo, text=afiliaciones, font=self.myFont8, bg="#1f1f1f", fg="#FFFFFF", wraplength=400, justify="left").grid(row=5, column=1, padx=20, pady=10, sticky="w")
        tk.Label(self.frameInfo, text=poderes, font=self.myFont8, bg="#1f1f1f", fg="#FFFFFF", wraplength=400, justify="left").grid(row=6, column=1, padx=20, pady=10, sticky="w")
        tk.Label(self.frameInfo, text=historia, font=self.myFont8, bg="#1f1f1f", fg="#FFFFFF", wraplength=400, justify="left").grid(row=7, column=1, padx=20, pady=10, sticky="w")
        tk.Label(self.frameInfo, text=aliados, font=self.myFont8, bg="#1f1f1f", fg="#FFFFFF", wraplength=400, justify="left").grid(row=8, column=1, padx=20, pady=10, sticky="w")
        tk.Label(self.frameInfo, text=enemigos, font=self.myFont8, bg="#1f1f1f", fg="#FFFFFF", wraplength=400, justify="left").grid(row=9, column=1, padx=20, pady=10, sticky="w")


    # Abre el editor de personajes
    def abrirEditor(self):
        self.editor = tk.Toplevel(self.personajes)

        self.editor.title("Comic Universe: Editor de Personajes")

        self.editor.geometry("600x600")

        self.editor.configure(bg="#121212")

        labelTitulo = tk.Label(self.editor, text="Editor de Personajes ", font=self.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        tk.Label(self.editor, text="Elija el personaje a editar / eliminar ", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF").place(x=40, y=100)

        self.selPersonajeE = ttk.Combobox(self.editor, state="readonly", width=30, font=self.myFont3, values=self.getPersonajes())
        self.selPersonajeE.place(x = 40, y=140)

        # Editar
        self.frameEditar = tk.Frame(self.editor, bg="#1f1f1f", width=250, height=400)
        self.frameEditar.place(x=40, y=180)

        tk.Label(self.frameEditar, text="Editar Personaje", fg = "#FFFFFF", bg="#1f1f1f", font=self.myFont7).place(relx = 0.01, rely=0.01, anchor="nw")

        lblEditar = tk.Label(self.frameEditar, text="Elija la característica a modificar.", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF", wraplength=175, justify="center")
        lblEditar.place(relx = 0.5, rely=0.2, anchor="center")

        self.selEditar = ttk.Combobox(self.frameEditar, state="readonly", width=20, font=self.myFont3, values=["edad", "cumple", "lugar de origen", "afiliaciones", "habilidades", "historia", "aliados", "enemigos"])
        self.selEditar.place(relx = 0.5, rely=0.3, anchor="center")

        lblEntry = tk.Label(self.frameEditar, text="Ingrese el nuevo valor.", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF", wraplength=175, justify="center")
        lblEntry.place(relx = 0.5, rely=0.5, anchor="center")

        self.entryEditar = tk.Entry(self.frameEditar, width=20, font= self.myFont3)
        self.entryEditar.place(relx = 0.5, rely=0.6, anchor="center")

        btnEditar = tk.Button(self.frameEditar, text="Editar", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.editarPersonaje())
        btnEditar.place(relx = 0.5, rely=0.8, anchor="center")

        # Eliminar
        self.frameEliminar = tk.Frame(self.editor, bg="#1f1f1f", width=250, height=400)
        self.frameEliminar.place(x=310, y=180)

        tk.Label(self.frameEliminar, text="Eliminar Personaje", fg = "#FFFFFF", bg="#1f1f1f", font=self.myFont7).place(relx = 0.01, rely=0.01, anchor="nw")

        lblEliminar = tk.Label(self.frameEliminar, text="Cuidado. Solo se puede eliminar el personaje si no existe en ningun comic.", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF", wraplength=150, justify="center")
        lblEliminar.place(relx = 0.5, rely=0.3, anchor="center")

        btnEliminar = tk.Button(self.frameEliminar, text="Eliminar", font=self.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.eliminarPersonaje())
        btnEliminar.place(relx = 0.5, rely=0.6, anchor="center")


    # Edita la característica del personaje seleccionada
    def editarPersonaje(self):
        personaje = self.selPersonajeE.get()
        caracteristica = self.selEditar.get()

        if personaje != "" and caracteristica != "":
            file = archivo("personajes.txt")
            lista = file.contenido
            lista = eval(lista)

            for item in lista:
                if item["nombre"] == personaje:
                    item[caracteristica] = self.entryEditar.get()
                    break

            file.contenido = str(lista)
            file.escribir()


    # Elimina el personaje seleccionado si no está en uso
    def eliminarPersonaje(self):
        personaje = self.selPersonajeE.get()

        try:
            self.lblError
            self.lblError.destroy()
        except:
            pass

        if personaje != "":
            lista = archivo("personajes.txt").contenido
            lista = eval(lista)

            for item in lista:
                if item["nombre"] == personaje:
                    if item["nombre"] in self.getPersonajesEnUso():
                        self.lblError = tk.Label(self.frameEliminar, text="El personaje no se puede eliminar porque está en uso", font=self.myFont3, bg="#1f1f1f", fg="#d6292f", wraplength=150, justify="center")
                        self.lblError.place(relx = 0.5, rely=0.8, anchor="center")
                        return

                    lista.remove(item)
                    break

        file = archivo("personajes.txt")
        file.contenido = str(lista)
        file.escribir()


    # Retorna una lista con todos los personajes que existen en los comics
    # S: lista con los nombres de los personajes
    def getPersonajesEnUso(self):
        res = []

        for comic in self.getComics():
            file = comicFile(comic)
            lista = eval(file.contenido)

            for escena in lista["escenas"]:
                for dialogo in escena["dialogos"]:
                    personaje = dialogo["personaje"]
                    if personaje not in res:
                        res.append(personaje)

        return res


    # Obtiene los comics en el folder
    # S: lista con los nombres de los comics
    def getComics(self):
        directory = 'Proyecto 3\\comics'
        res = []

        files = Path(directory).glob('*')
        for file in files:
            filename = Path(file).stem
            res.append(filename)

        return res


    # Updatea la lista de personajes
    def updatePersonajes(self):
        enUso = self.getPersonajesEnUso()
        for personajeEnUso in enUso:
            if personajeEnUso in self.getPersonajes():
                continue
            else:
                filePerso = archivo("personajes.txt")
                listaPerso = filePerso.contenido
                listaPerso = eval(listaPerso)
                nuevoPerso = {"nombre": personajeEnUso, "edad": "-", "cumple": "-", "lugar de origen": "-", "afiliaciones": "-", "habilidades": "-", "historia": "-", "aliados": "-", "enemigos": "-"}

                listaPerso.append(nuevoPerso)
                filePerso.contenido = str(listaPerso)
                filePerso.escribir()



class Inicio(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#121212")

        self.controller = controller

        labelTitulo = tk.Label(self, text="Bienvenido a ComicUniverse! ", font=controller.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        labelCreditos = tk.Label(self, text="Creado por Javier Carrillo", font=controller.myFont4, bg="#121212", fg="#FFFFFF")
        labelCreditos.place(x=40, y=100)

        # Frame para el login
        loginFrame = tk.Frame(self, bg="#1f1f1f", width=500, height=400)
        loginFrame.place(x=150, y=250)
        loginFrame.grid_propagate(False)
        loginFrame.grid_columnconfigure(0, weight=1, pad=10)
        loginFrame.grid_rowconfigure(0, weight=1, pad=10)
        loginFrame.grid_rowconfigure(1, weight=1)
        loginFrame.grid_rowconfigure(4, weight=1)

        labelInstrucciones = tk.Label(loginFrame, text="Para ingresar a la aplicación,\n ingrese su usuario y contraseña", font=controller.myFont2, bg="#1f1f1f", fg="#FFFFFF")
        labelInstrucciones.grid(row=0, column=0, pady=10, sticky="nsew", columnspan=2)

        self.txtUsuario = tk.StringVar()
        labelUsuario = tk.Label(loginFrame, text="Usuario: ", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelUsuario.grid(row=2, column=0, pady=10, sticky="nsew", padx=20)
        entryUsuario = tk.Entry(loginFrame, width=25, font= controller.myFont3, textvariable=self.txtUsuario)
        entryUsuario.grid(row=2, column=1, pady=10, sticky="nsew", padx=20)

        self.txtContrasena = tk.StringVar()
        labelContrasena = tk.Label(loginFrame, text="Contraseña: ", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelContrasena.grid(row=3, column=0, pady=10, sticky="nsew")
        entryContrasena = tk.Entry(loginFrame, width=25, font= controller.myFont3, show="●", textvariable=self.txtContrasena)
        entryContrasena.grid(row=3, column=1, pady=10, sticky="nsew", padx=20)

        botonIngresar = tk.Button(loginFrame, text="Ingresar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.ingresar())
        botonIngresar.grid(row=4, column=0, pady=50, padx =50,sticky="nsew", columnspan=2)


    # Revisa si el usuario y contraseña ingresados son correctos
    def ingresar(self):
        global tipo

        # Obtener la información del archivo de usuarios
        fileKeys = archivo("usuarios.txt")
        fileKeys.desencriptar()
        keys = eval(fileKeys.contenido)
        fileKeys.encriptar()

        # Revisa si calza con algún usuario
        for key in keys:
            if (key["username"] == self.txtUsuario.get() and key["password"] == self.txtContrasena.get()):

                if key["tipo"] == "admin":
                    tipo = "rw"
                    self.controller.showFrame("Admin")
                elif key["tipo"] == "read":
                    tipo = "r"
                    self.controller.showFrame("Menu")
                elif key["tipo"] == "write":
                    tipo = "w"
                    self.controller.showFrame("Menu")
                elif key["tipo"] == "read/write":
                    tipo = "rw"
                    self.controller.showFrame("Menu")

                self.txtUsuario.set("")
                self.txtContrasena.set("")
                return

        # Mostrar mensaje de error
        labelError = tk.Label(self, text="Usuario y/o contraseña incorrecto(s)", font=self.controller.myFont3, bg="#121212", fg="#d6292f")
        labelError.place(x=150, y=700)
        self.update()
        time.sleep(1)
        labelError.destroy()





class Admin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#121212")

        self.controller = controller

        self.readKeys()
        self.getLista()

        labelTitulo = tk.Label(self, text="Administrador ", font=controller.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        # Crear nuevo
        frameNew = tk.Frame(self, bg="#1f1f1f", width=350, height=400)
        frameNew.place(x=40, y=130)
        frameNew.grid_propagate(False)
        frameNew.grid_columnconfigure(0, weight=1, pad=10)
        frameNew.grid_columnconfigure(1, weight=5, pad=10)

        tk.Label(frameNew, text= "Crear Usuario", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont7).grid(row=0, column=0, pady=10, columnspan=2)

        labelNew1 = tk.Label(frameNew, text="Nombre:", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelNew1.grid(row=1, column=0, padx=20, pady=10)

        entryNew1 = tk.Entry(frameNew, font= controller.myFont3)
        entryNew1.grid(row=1, column=1, padx=20, pady=10)

        labelNew2 = tk.Label(frameNew, text="Contraseña:", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelNew2.grid(row=2, column=0, padx=20, pady=10)

        entryNew2 = tk.Entry(frameNew, font= controller.myFont3, show="●")
        entryNew2.grid(row=2, column=1, padx=20, pady=10)

        labelNew3 = tk.Label(frameNew, text="Tipo:", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelNew3.grid(row=3, column=0, padx=20, pady=10)

        selectNew = ttk.Combobox(frameNew, state="readonly", font=controller.myFont3, values=["admin", "read", "write", "read/write"])
        selectNew.grid(row=3, column=1, padx=20, pady=10)

        btnNew = tk.Button(frameNew, text="Crear", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.crear(entryNew1.get(), entryNew2.get(), selectNew.get()))
        btnNew.grid(row=6, column=0, pady=10, padx=20,columnspan=2)

        # Eliminar
        frameDel = tk.Frame(self, bg="#1f1f1f", width=350, height=400)
        frameDel.place(x=400, y=130)
        frameDel.grid_propagate(False)
        frameDel.grid_columnconfigure(0, weight=1, pad=10)

        tk.Label(frameDel, text= "Eliminar Usuario", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont7).grid(row=0, column=0, pady=10)

        labelDel = tk.Label(frameDel, text="Elija el usuario a eliminar:", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelDel.grid(row=1, column=0, padx=20)

        self.selectDel = ttk.Combobox(frameDel, state="readonly", width=20, font=controller.myFont3, values=self.lista)
        self.selectDel.grid(row=2, column=0, padx=20)

        btnDel = tk.Button(frameDel, text="Eliminar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.eliminar(self.selectDel.get()))
        btnDel.grid(row=6, column=0, pady=10, padx=20)

        # Modificar
        frameMod = tk.Frame(self, bg="#1f1f1f", width=350, height=280)
        frameMod.place(x=40, y=540)
        frameMod.grid_propagate(False)
        frameMod.grid_columnconfigure(0, weight=1, pad=10)

        tk.Label(frameMod, text= "Modificar Usuario", fg = "#FFFFFF",bg="#1f1f1f", font=controller.myFont7).grid(row=0, column=0, pady=10)

        labelMod1 = tk.Label(frameMod, text="Elija el usuario a modificar:", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelMod1.grid(row=1, column=0, padx=20)

        self.selectMod1 = ttk.Combobox(frameMod, state="readonly", width=20, font=controller.myFont3, values=self.lista)
        self.selectMod1.grid(row=2, column=0, padx=20)

        tk.Label(frameMod, bg="#1f1f1f").grid(row=3, column=0, pady=10)

        labelMod2 = tk.Label(frameMod, text="Elija el tipo de permiso:", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelMod2.grid(row=4, column=0, padx=20)

        selectMod2 = ttk.Combobox(frameMod, state="readonly", width=20, font=controller.myFont3, values=["admin", "read", "write", "read/write"])
        selectMod2.grid(row=5, column=0, padx=20)

        btnMod = tk.Button(frameMod, text="Modificar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.modificar(self.selectMod1.get(), selectMod2.get()))
        btnMod.grid(row=6, column=0, pady=10, padx=20)

        # Lista de usuarios
        self.frameList = tk.Frame(self, bg="#1f1f1f", width=350, height=280)
        self.frameList.place(x=400, y=540)
        self.frameList.grid_propagate(False)
        self.frameList.grid_columnconfigure(0, weight=1, pad=10)
        self.frameList.grid_columnconfigure(1, weight=1, pad=10)

        tk.Label(self.frameList, text= "Lista de Usuarios", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont7).grid(row=0, column=0, pady=10, columnspan=2)

        tk.Label(self.frameList, text="Nombre", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF").grid(row=1, column=0, padx=20)
        tk.Label(self.frameList, text="Tipo", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF").grid(row=1, column=1, padx=20)

        self.crearLista()

        # Botones
        btnAtras = tk.Button(self, text="Cerrar Sesión", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.showFrame("Inicio"))
        btnAtras.place(x=636, y=20)

        btnContinue = tk.Button(self, text="Continuar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.showFrame("Menu"))
        btnContinue.place(x=667, y=850)


    # Crea un nuevo usuario
    def crear(self, nombre, password, tipo):
        self.keys.append({"username": nombre, "password": password, "tipo": tipo})
        self.writeKeys()
        self.updateValues()
        self.destruirLista()
        self.crearLista()


    # Elimina un usuario
    def eliminar(self, usuario):
        for key in self.keys:
            if key["username"] == usuario:
                self.keys.remove(key)
                break
        self.writeKeys()
        self.updateValues()
        self.destruirLista()
        self.crearLista()


    # Modifica el tipo de permiso de un usuario
    def modificar(self, usuario, tipo):
        for key in self.keys:
            if key["username"] == usuario:
                key["tipo"] = tipo
                break
        self.writeKeys()
        self.updateValues()
        self.destruirLista()
        self.crearLista()


    # Obtiene la información del archivo
    def readKeys(self):
        fileKeys = archivo("usuarios.txt")
        fileKeys.desencriptar()
        self.keys = eval(fileKeys.contenido)
        fileKeys.encriptar()


    # Guarda la información en el archivo
    def writeKeys(self):
        fileKeys = archivo("usuarios.txt")
        fileKeys.desencriptar()
        fileKeys.contenido = str(self.keys)
        fileKeys.escribir()
        fileKeys.encriptar()


    # Obtiene los valores de los usuarios y los guarda en una lista
    def getLista(self):
        self.lista = []
        for key in self.keys:
            self.lista.append(key["username"])


    # Actualiza los valores de los usuarios en los selectores
    def updateValues(self):
        self.getLista()
        self.selectDel.config(values=self.lista)
        self.selectMod1.config(values=self.lista)


    # Crea la lista de usuarios
    def crearLista(self):
        contador = 2
        self.users = []
        self.tipos = []
        for key in self.keys:
            self.users.append(tk.Label(self.frameList, text=key["username"], font=self.controller.myFont4, bg="#1f1f1f", fg="#FFFFFF"))
            self.users[contador - 2].grid(row=contador, column=0, padx=20)

            self.tipos.append(tk.Label(self.frameList, text=key["tipo"], font=self.controller.myFont4, bg="#1f1f1f", fg="#FFFFFF"))
            self.tipos[contador - 2].grid(row=contador, column=1, padx=20)

            contador += 1


    # Destruye la lista de usuarios
    def destruirLista(self):
        for user in self.users:
            user.destroy()
        for tipo in self.tipos:
            tipo.destroy()





class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#121212")

        self.controller = controller

        labelTitulo = tk.Label(self, text="Menu ", font=controller.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        btnAtras = tk.Button(self, text="Cerrar Sesión", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.showFrame("Inicio"))
        btnAtras.place(x=636, y=20)

        # Frame Leer
        frameLeer = tk.Frame(self, bg="#1f1f1f", width=350, height=600)
        frameLeer.place(x=40, y=130)
        frameLeer.grid_propagate(False)
        frameLeer.grid_columnconfigure(0, weight=1, pad=10)
        frameLeer.grid_rowconfigure(0, weight=1, pad=10)

        # Frame Escribir
        frameEscribir = tk.Frame(self, bg="#1f1f1f", width=350, height=600)
        frameEscribir.place(x=400, y=130)
        frameEscribir.grid_propagate(False)
        frameEscribir.grid_columnconfigure(0, weight=1, pad=10)
        frameEscribir.grid_rowconfigure(0, weight=1, pad=10)

        self.btnLeer = tk.Button(frameLeer, text="Leer un Comic", font=controller.myFont6, state="disabled",bg="#0d1934", fg="#FFFFFF", relief="groove", command=lambda: controller.showFrame("MenuLeer"))
        self.btnLeer.grid(row=0, column=0, padx=20, pady=10, sticky='nesw')

        self.btnEscribir = tk.Button(frameEscribir, text="Editar o Crear un Comic", font=controller.myFont6, state="disabled", bg="#300723", fg="#FFFFFF", relief="groove", command=lambda: controller.showFrame("MenuTweak"))
        self.btnEscribir.grid(row=0, column=0, padx=20, pady=10, sticky='nesw')

        tk.Button(self, text="Activar botones", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.setButtons()).place(relx=0.5, y=850, anchor="center")

    def setButtons(self):
        global tipo
        if tipo == "r":
            self.btnEscribir.config(state="disabled")
            self.btnLeer.config(state="normal")
        elif tipo == "w":
            self.btnEscribir.config(state="normal")
            self.btnLeer.config(state="disabled")
        elif tipo == "rw":
            self.btnEscribir.config(state="normal")
            self.btnLeer.config(state="normal")





class MenuLeer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#121212")

        self.controller = controller

        labelTitulo = tk.Label(self, text="Leer un Comic ", font=controller.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        btnAtras = tk.Button(self, text="Cerrar Sesión", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.showFrame("Inicio"))
        btnAtras.place(x=636, y=20)

        btnMenu = tk.Button(self, text="Regresar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.showFrame("Menu"))
        btnMenu.place(x= 670, y= 60)

        # Seleccionar el Comic
        frameComic = tk.Frame(self, bg="#1f1f1f", width=350, height=250)
        frameComic.place(x=40, y=130)
        frameComic.grid_propagate(False)
        frameComic.grid_columnconfigure(0, weight=1, pad=10)

        tk.Label(frameComic, text= "Comic", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont7).grid(row=0, column=0, pady=10)

        labelBuscar = tk.Label(frameComic, text="Filtrar:", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelBuscar.grid(row=1, column=0, padx=20, sticky="e")

        entryBuscar = tk.Entry(frameComic, font= controller.myFont3)
        entryBuscar.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        btnBuscar = tk.Button(frameComic, text="Buscar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.filtrar(entryBuscar.get()))
        btnBuscar.grid(row=2, column=0, pady=10, padx=20)

        btnBuscarPerso = tk.Button(frameComic, text="Buscar Personaje", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.filtrarPersonaje(entryBuscar.get()))
        btnBuscarPerso.grid(row=2, column=1, pady=10, padx=20)

        labelComic = tk.Label(frameComic, text="Elija el comic a leer:", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelComic.grid(row=3, column=0, padx=20, columnspan=2)

        self.selectComic = ttk.Combobox(frameComic, state="readonly", width=30, font=controller.myFont3, values=self.getComics())
        self.selectComic.grid(row=4, column=0, padx=20, columnspan=2)
        self.selectComic.bind("<<ComboboxSelected>>", lambda event: self.getInfo(self.selectComic.get(), event))

        # Seleccionar Forma de Lectura
        frameLector = tk.Frame(self, bg="#1f1f1f", width=350, height=250)
        frameLector.place(x=400, y=130)
        frameLector.grid_propagate(False)
        frameLector.grid_columnconfigure(0, weight=1, pad=10)

        tk.Label(frameLector, text= "Formato", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont7).grid(row=0, column=0, pady=10)

        labelLector = tk.Label(frameLector, text="Elija el formato con el que quiere leer:", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        labelLector.grid(row=1, column=0, padx=20)

        selectLector = ttk.Combobox(frameLector, state="readonly", width=20, font=controller.myFont3, values=["Por Diálogo", "Por Escena", "Por Página"])
        selectLector.grid(row=2, column=0, padx=20)

        # Información del Comic
        self.frameInfo = tk.Frame(self, bg="#1f1f1f", width=710, height=450)
        self.frameInfo.place(x=40, y=390)
        self.frameInfo.grid_propagate(False)

        tk.Label(self.frameInfo, text= "Información", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont7).grid(row=0, column=0, pady=10, padx=20, sticky="w")

        lblNombre = tk.Label(self.frameInfo, text="Nombre: ", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblNombre.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        lblAutor = tk.Label(self.frameInfo, text="Autor: ", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblAutor.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        lblFecha = tk.Label(self.frameInfo, text="Fecha: ", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblFecha.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        lblDescripcion = tk.Label(self.frameInfo, text="Descripción: ", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblDescripcion.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        # Boton para ver personajes
        btnPersonajes = tk.Button(self, text="Personajes", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.abrirPersonajes())
        btnPersonajes.place(x=40, y=850)

        # Boton para ingresar
        btnContinue = tk.Button(self, text="Ingresar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.leerComic(self.selectComic.get(), selectLector.get()))
        btnContinue.place(x=675, y=850)


    # Obtiene los comics para el selector
    def getComics(self):
        directory = 'Proyecto 3\\comics'
        res = []

        files = Path(directory).glob('*')
        for file in files:
            filename = Path(file).stem
            res.append(filename)

        return res


    # Obtiene la información del comic seleccionado
    # E: nombre del comic
    def getInfo(self, comic, event=None):
        contenido = comicFile(comic).contenido
        contenido = eval(contenido)

        self.frameInfo.destroy()

        self.frameInfo = tk.Frame(self, bg="#1f1f1f", width=710, height=450)
        self.frameInfo.place(x=40, y=390)
        self.frameInfo.grid_propagate(False)

        tk.Label(self.frameInfo, text= "Información", fg = "#FFFFFF", bg="#1f1f1f", font=self.controller.myFont7).grid(row=0, column=0, pady=10, padx=20, sticky="w")

        lblNombre = tk.Label(self.frameInfo, text="Nombre: ", font=self.controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblNombre.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        lblAutor = tk.Label(self.frameInfo, text="Autor: ", font=self.controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblAutor.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        lblFecha = tk.Label(self.frameInfo, text="Fecha: ", font=self.controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblFecha.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        lblDescripcion = tk.Label(self.frameInfo, text="Descripción: ", font=self.controller.myFont3, bg="#1f1f1f", fg="#FFFFFF")
        lblDescripcion.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        nombre = contenido["info"]["nombre"]
        tk.Label(self.frameInfo, text=nombre, font=self.controller.myFont3, bg="#1f1f1f", fg="#FFFFFF").grid(row=1, column=1, padx=20, pady=10, sticky="w")

        autor = contenido["info"]["autor"]
        tk.Label(self.frameInfo, text=autor, font=self.controller.myFont3, bg="#1f1f1f", fg="#FFFFFF").grid(row=2, column=1, padx=20, pady=10, sticky="w")

        fecha = contenido["info"]["fecha"]
        tk.Label(self.frameInfo, text=fecha, font=self.controller.myFont3, bg="#1f1f1f", fg="#FFFFFF").grid(row=3, column=1, padx=20, pady=10, sticky="w")

        descripcion = contenido["info"]["descripcion"]
        tk.Label(self.frameInfo, text=descripcion, font=self.controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", wraplength=470, justify="left").grid(row=4, column=1, padx=20, pady=10, sticky="w")


    # Filtra las selecciones de los comics
    # E: str
    def filtrar(self, str):
        directory = 'Proyecto 3\\comics'
        res = []

        files = Path(directory).glob('*')
        for file in files:
            filename = Path(file).stem
            if str.lower() in filename.lower():
                res.append(filename)

        self.selectComic.config(values=res)


    # Filtra las selecciones de los comics por personaje
    # E: str
    def filtrarPersonaje(self, str):
        directory = 'Proyecto 3\\comics'
        res = []

        files = Path(directory).glob('*')
        for file in files:
            filename = Path(file).stem
            contenido = comicFile(filename).contenido
            contenido = eval(contenido)
            for escena in contenido["escenas"]:
                for dialogo in escena["dialogos"]:
                    if str.lower() in dialogo["personaje"].lower():
                        if filename not in res:
                            res.append(filename)
                        break

        self.selectComic.config(values=res)


    # Comienza la lectura de un comic
    # E: comic, formato (strings)
    def leerComic(self, strComic, strFormato):
        global comic
        global formato
        global contents
        if strComic != "" and strFormato != "":
            comic = strComic
            formato = strFormato
            contents = comicFile(comic).contenido
            contents = eval(contents)
            self.controller.showFrame("Lector")





class Lector(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#121212")

        self.controller = controller

        labelTitulo = tk.Label(self, text="Lector ", font=controller.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        # Botones
        btnMenu = tk.Button(self, text="Regresar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.reset())
        btnMenu.place(x= 670, y= 60)

        self.btnComenzar = tk.Button(self, text="Comenzar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.comenzar())
        self.btnComenzar.place(x= 670, y= 850)

        btnPersonajes = tk.Button(self, text="Personajes", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.abrirPersonajes())
        btnPersonajes.place(x=40, y=850)


    # Comienza la lectura
    def comenzar(self):
        self.variables()

        if formato == "Por Diálogo":
            self.enseñarDialogo()

            self.btnSeguir = tk.Button(self, text="⏩", font=self.controller.myFont9, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.mostrarSiguienteDialogo(), relief="flat")
            self.btnSeguir.place(relx=0.57, y= 750, anchor="center")

            self.btnAtras = tk.Button(self, text="⏪", font=self.controller.myFont9, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.mostrarAnteriorDialogo(), relief="flat")
            self.btnAtras.place(relx=0.43, y= 750, anchor="center")

        elif formato == "Por Escena":
            self.enseñarEscena()

            self.btnSeguir = tk.Button(self, text="⏩", font=self.controller.myFont9, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.mostrarSiguienteEscena(), relief="flat")
            self.btnSeguir.place(relx=0.57, y= 750, anchor="center")

            self.btnAtras = tk.Button(self, text="⏪", font=self.controller.myFont9, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.mostrarAnteriorEscena(), relief="flat")
            self.btnAtras.place(relx=0.43, y= 750, anchor="center")

        elif formato == "Por Página":
            self.enseñarPagina()

            self.btnSeguir = tk.Button(self, text="⏩", font=self.controller.myFont9, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.mostrarSiguientePagina(), relief="flat")
            self.btnSeguir.place(relx=0.57, y= 750, anchor="center")

            self.btnAtras = tk.Button(self, text="⏪", font=self.controller.myFont9, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.mostrarAnteriorPagina(), relief="flat")
            self.btnAtras.place(relx=0.43, y= 750, anchor="center")

        self.btnComenzar.destroy()


    # Resetea variables
    def variables(self):
        self.pag = 0
        self.escena = 0
        self.dialogo = 0


    # Resetea la lectura
    def reset(self):

        if formato == "Por Diálogo":
            self.destruirLabels()
            self.destruirBotones()
        elif formato == "Por Escena":
            self.destruirLabelsE()
            self.destruirBotones()
        elif formato == "Por Página":
            self.destruirLabelsP()
            self.destruirBotones()
            try:
                self.selDialogos
                self.selDialogos.destroy()
            except:
                pass

            try:
                self.selEscenas
                self.selEscenas.destroy()
            except:
                pass

        self.variables()
        self.controller.showFrame("MenuLeer")

        if self.btnComenzar.winfo_exists() == 0:
            self.btnComenzar = tk.Button(self, text="Comenzar", font=self.controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.comenzar())
            self.btnComenzar.place(x= 670, y= 850)


    # Pone la imagen
    def ponerImagen(self, imageName):
        image = Image.open(imageName)

        baseheight = 350
        hpercent = (baseheight/float(image.size[1]))
        wsize = int((float(image.size[0])*float(hpercent)))
        image = image.resize((wsize, baseheight), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self, image=photo)
        self.label.photo = photo
        self.label.place(relx=0.5, rely=0.45, anchor="center")


    # POR PAGINA _______________________________________________________________________________________________
    #____________________________________________________________________________________________________________
    # Enseñar pagina
    def enseñarPagina(self):
        global contents
        pag = self.pag + 1

        self.lblPag = tk.Label(self, text="Página: " + str(pag), font=self.controller.myFont4, bg="#121212", fg="#FFFFFF")
        self.lblPag.place(x=150, y=200)

        self.obtenerEscenas()


    # Obtiene las escenas de una página y las coloca en un selector
    def obtenerEscenas(self):
        global contents
        res = []
        try:
            self.selEscenas
            self.selEscenas.destroy()
        except:
            pass

        for escena in contents["escenas"]:
            if escena["pag"] == self.pag + 1:
                res.append("Escena " + str(escena["num"]))

        self.selEscenas = ttk.Combobox(self, state="readonly", width=20, font=self.controller.myFont3, values=res)
        self.selEscenas.place(relx=0.4, y= 210, anchor="center")

        self.selEscenas.bind("<<ComboboxSelected>>", lambda x: self.mostrarEscena(x))


    # Muestra la escena seleccionada
    def mostrarEscena(self, event=None):
        global contents
        pag = self.pag + 1
        esc = int(self.selEscenas.get()[-1:])
        self.escena = esc - 1

        self.destruirLabelsP()

        if contents["info"]["prefijo"] != "":
            imageName = "C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\Imagenes\\" + contents["info"]["prefijo"] + "_" + str(pag) + "_0" + str(esc) + ".png"
            self.ponerImagen(imageName)

        self.obtenerDialogosP()


    # Obtiene la siguiente pagina
    def siguientePagina(self):
        global contents
        newpag = self.pag + 2

        for escena in contents["escenas"]:
            if escena["pag"] == newpag:
                self.pag += 1
                return


    # Obtiene la pagina anterior
    def anteriorPagina(self):
        if self.pag != 0:
            self.pag -= 1


    # Muestra la siguiente pagina
    def mostrarSiguientePagina(self):
        self.siguientePagina()
        self.destruirLabelsP()
        self.enseñarPagina()
        try:
            self.selDialogos
            self.selDialogos.destroy()
        except:
            pass


    # Muestra la pagina anterior
    def mostrarAnteriorPagina(self):
        self.anteriorPagina()
        self.destruirLabelsP()
        self.enseñarPagina()


    # Destruye las labels
    def destruirLabelsP(self):
        try:
            self.label
            self.label.destroy()
        except:
            pass

        try:
            self.lblDialogo
            self.lblDialogo.destroy()
        except:
            pass




    # Obtiene Dialogos de una escena
    def obtenerDialogosP(self):
        global contents
        res = []

        try:
            self.selDialogos
            self.selDialogos.destroy()
        except AttributeError:
            pass

        for escena in contents["escenas"]:
            if escena["pag"] == self.pag + 1 and escena["num"] == self.escena + 1:
                for dialogo in escena["dialogos"]:
                    text = dialogo["personaje"] + ": " + dialogo["contenido"]

                    res.append(text)

        self.selDialogos = ttk.Combobox(self, state="readonly", width=50, font=self.controller.myFont3, values=res)
        self.selDialogos.place(relx=0.5, y= 600, anchor="center")

        self.selDialogos.bind("<<ComboboxSelected>>", lambda x: self.mostrarDialogo(x))


    # POR ESCENA ________________________________________________________________________________________________
    #____________________________________________________________________________________________________________
    # Enseñar Escena
    def enseñarEscena(self):
        global contents
        pag = contents["escenas"][self.escena]["pag"]
        esc = contents["escenas"][self.escena]["num"]

        if contents["info"]["prefijo"] != "":
            imageName = "C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\Imagenes\\" + contents["info"]["prefijo"] + "_" + str(pag) + "_0" + str(esc) + ".png"
            self.ponerImagen(imageName)

        self.lblPag = tk.Label(self, text="Página: " + str(pag), font=self.controller.myFont4, bg="#121212", fg="#FFFFFF")
        self.lblPag.place(x=150, y=200)

        self.lblEscena = tk.Label(self, text="Escena: " + str(esc), font=self.controller.myFont4, bg="#121212", fg="#FFFFFF")
        self.lblEscena.place(x=230, y=200)

        self.obtenerDialogos()


    # Obtiene los dialogos de una escena y los coloca en un selector
    def obtenerDialogos(self):
        global contents
        res = []

        try:
            self.selDialogos
            self.selDialogos.destroy()
        except AttributeError:
            pass

        for dialogo in contents["escenas"][self.escena]["dialogos"]:

            text = dialogo["personaje"] + ": " + dialogo["contenido"]

            res.append(text)

        self.selDialogos = ttk.Combobox(self, state="readonly", width=50, font=self.controller.myFont3, values=res)
        self.selDialogos.place(relx=0.5, y= 600, anchor="center")

        self.selDialogos.bind("<<ComboboxSelected>>", lambda x: self.mostrarDialogo(x))


    # Muestra el dialogo seleccionado
    def mostrarDialogo(self, event=None):
        if self.selDialogos.get() == "":
            return

        try:
            self.lblDialogo
            self.lblDialogo.destroy()
        except AttributeError:
            pass

        self.lblDialogo = tk.Label(self, text=self.selDialogos.get(), font=self.controller.myFont3, bg="#121212", fg="#FFFFFF", wraplength=600, justify="left")
        self.lblDialogo.place(relx=0.5, y=650, anchor="center")


    # Obtiene la siguiente escena
    def siguienteEscena(self):
        global contents
        try:
            contents["escenas"][self.escena + 1]["dialogos"][self.dialogo]
            self.escena += 1
        except:
            return -1


    # Obtiene la escena anterior
    def anteriorEscena(self):
        global contents
        if self.escena == 0:
            return -1
        self.escena -= 1


    # Muestra la siguiente escena
    def mostrarSiguienteEscena(self):
        if self.siguienteEscena() != -1:
            self.destruirLabelsE()
            self.enseñarEscena()


    # Muestra la escena anterior
    def mostrarAnteriorEscena(self):
        if self.anteriorEscena() != -1:
            self.destruirLabelsE()
            self.enseñarEscena()


    # Destruye las labels
    def destruirLabelsE(self):
        try:
            self.label
            self.label.destroy()
        except:
            pass

        try:
            self.lblPag
            self.lblPag.destroy()
            self.lblEscena.destroy()
            self.selDialogos.destroy()
        except:
            pass

        try:
            self.lblDialogo
            self.lblDialogo.destroy()
        except AttributeError:
            pass


    # POR DIALOGO _______________________________________________________________________________________________
    #____________________________________________________________________________________________________________
    # Siguiente Dialogo
    def siguienteDialogo(self):
        global contents
        try:
            contents["escenas"][self.escena]["dialogos"][self.dialogo + 1]
            self.dialogo += 1
        except IndexError:
            try:
                self.dialogo = 0
                contents["escenas"][self.escena + 1]["dialogos"][self.dialogo]
                self.escena += 1
            except IndexError:
                return -1


    # Dialogo Anterior
    def anteriorDialogo(self):
        global contents
        primerEsc = self.escena == 0
        primerDialogo = self.dialogo == 0

        if not primerDialogo:
            self.dialogo -= 1
            return
        elif not primerEsc:
            self.escena -= 1
            num = len(contents["escenas"][self.escena]["dialogos"])
            self.dialogo = num - 1
            return


    # Enseñar Dialogo
    def enseñarDialogo(self):
        global contents
        pag = contents["escenas"][self.escena]["pag"]
        esc = contents["escenas"][self.escena]["num"]
        dialogo = contents["escenas"][self.escena]["dialogos"][self.dialogo]

        if contents["info"]["prefijo"] != "":
            imageName = "C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\Imagenes\\" + contents["info"]["prefijo"] + "_" + str(pag) + "_0" + str(esc) + ".png"
            self.ponerImagen(imageName)

        self.lblPag = tk.Label(self, text="Página: " + str(pag), font=self.controller.myFont4, bg="#121212", fg="#FFFFFF")
        self.lblPag.place(x=150, y=200)

        self.lblEscena = tk.Label(self, text="Escena: " + str(esc), font=self.controller.myFont4, bg="#121212", fg="#FFFFFF")
        self.lblEscena.place(x=230, y=200)

        text = dialogo["personaje"] + ": " + dialogo["contenido"]
        self.lblDialogo = tk.Label(self, text=text, font=self.controller.myFont3, bg="#121212", fg="#FFFFFF", wraplength=600, justify="left")
        self.lblDialogo.place(x=100, y=600)


    # Destruir Labels
    def destruirLabels(self):
        try:
            self.label
            self.label.destroy()
        except:
            pass

        try:
            self.lblPag
            self.lblPag.destroy()
            self.lblEscena.destroy()
            self.lblDialogo.destroy()
        except AttributeError:
            return


    # Destruir botones
    def destruirBotones(self):
        try:
            self.btnSeguir
            self.btnSeguir.destroy()
            self.btnAtras.destroy()
        except AttributeError:
            return


    # Muestra el siguiente dialogo
    def mostrarSiguienteDialogo(self):
        if self.siguienteDialogo() == -1:
            return
        self.destruirLabels()
        self.enseñarDialogo()


    # Muestra el dialogo anterior
    def mostrarAnteriorDialogo(self):
        self.anteriorDialogo()
        self.destruirLabels()
        self.enseñarDialogo()





class MenuTweak(tk.Frame):

     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#121212")

        self.controller = controller

        labelTitulo = tk.Label(self, text="Editar y Crear Comics ", font=controller.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        btnAtras = tk.Button(self, text="Cerrar Sesión", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.showFrame("Inicio"))
        btnAtras.place(x=636, y=20)

        btnMenu = tk.Button(self, text="Regresar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.showFrame("Menu"))
        btnMenu.place(x= 670, y= 60)

        # Frame Leer
        frameEditar = tk.Frame(self, bg="#1f1f1f", width=350, height=600)
        frameEditar.place(x=40, y=130)
        frameEditar.grid_propagate(False)
        frameEditar.grid_columnconfigure(0, weight=1, pad=10)
        frameEditar.grid_rowconfigure(0, weight=1, pad=10)

        # Frame Escribir
        frameCrear = tk.Frame(self, bg="#1f1f1f", width=350, height=600)
        frameCrear.place(x=400, y=130)
        frameCrear.grid_propagate(False)
        frameCrear.grid_columnconfigure(0, weight=1, pad=10)
        frameCrear.grid_rowconfigure(0, weight=1, pad=10)

        self.btnEditar = tk.Button(frameEditar, text="✍Editar✍", font=controller.myFont5, bg="#871517", fg="#FFFFFF", relief="groove", command=lambda: controller.showFrame("MenuEditar"))
        self.btnEditar.grid(row=0, column=0, padx=20, pady=10, sticky='nesw')

        self.btnCrear = tk.Button(frameCrear, text="🆕Crear🆕", font=controller.myFont5, bg="#8a4a10", fg="#FFFFFF", relief="groove", command=lambda: controller.showFrame("MenuCrear"))
        self.btnCrear.grid(row=0, column=0, padx=20, pady=10, sticky='nesw')





class MenuCrear(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#121212")

        self.controller = controller

        self.pag = 1

        self.esc = 1

        self.res = {"info": {"nombre": "", "autor": "", "fecha": "", "descripcion": "", "prefijo": ""}, "escenas": [] }

        labelTitulo = tk.Label(self, text="Crear ", font=controller.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        btnAtras = tk.Button(self, text="Cerrar Sesión", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.showFrame("Inicio"))
        btnAtras.place(x=636, y=20)

        btnMenu = tk.Button(self, text="Regresar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: controller.showFrame("MenuTweak"))
        btnMenu.place(x= 670, y= 60)

        frameComic = tk.Frame(self, bg="#121212")
        frameComic.place(relx = 0.5, rely=0.55, anchor="center")

        # Paginas
        framePaginas = tk.Frame(frameComic, bg="#1f1f1f", width=700, height=350)
        framePaginas.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        tk.Label(framePaginas, text= "Ahora escribiendo en:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont7).place(x=10, y= 10, anchor="nw")

        self.lblPag = tk.Label(framePaginas, text="Página " + str(self.pag), font=controller.myFont7, bg="#1f1f1f", fg="#FFFFFF")
        self.lblPag.place(x=300, y=10, anchor="nw")

        self.lblEscena = tk.Label(framePaginas, text="Escena " + str(self.esc), font=controller.myFont7, bg="#1f1f1f", fg="#FFFFFF")
        self.lblEscena.place(x=450, y=10, anchor="nw")

        tk.Label(framePaginas, text= "Personaje:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(x=30, y= 75, anchor="nw")

        self.entryPersonaje = tk.Entry(framePaginas, width=15, font=controller.myFont3)
        self.entryPersonaje.place(x=30, y= 100, anchor="nw")

        tk.Label(framePaginas, text= "Diálogo:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(x=200, y= 75, anchor="nw")

        self.entryDialogo = tk.Entry(framePaginas, width=50, font=controller.myFont3)
        self.entryDialogo.place(x=200, y= 100, anchor="nw")

            # Botones
        btnAdjuntar = tk.Button(framePaginas, text="Adjuntar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.adjuntarDialogo(self.entryPersonaje.get(), self.entryDialogo.get()))
        btnAdjuntar.place(relx=0.5, y= 160, anchor="center")

        btnAntPag = tk.Button(framePaginas, text="Pagina Anterior", width= 20, font=controller.myFont10, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.anteriorPagina())
        btnAntPag.place(x = 100, y= 225, anchor="nw")

        btnSigPag = tk.Button(framePaginas, text="Pagina Siguiente", width= 20, font=controller.myFont10, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.siguientePagina())
        btnSigPag.place(x = 100, y= 275, anchor="nw")

        btnAntEsc = tk.Button(framePaginas, text="Escena Anterior", width= 20, font=controller.myFont10, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.anteriorEscena())
        btnAntEsc.place(x = 400, y= 225, anchor="nw")

        btnSigEsc = tk.Button(framePaginas, text="Escena Siguiente", width= 20, font=controller.myFont10, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.siguienteEscena())
        btnSigEsc.place(x = 400, y= 275, anchor="nw")

        self.lblError = tk.Label(framePaginas, text="", font=controller.myFont4, bg="#1f1f1f", fg="#af161a", justify="center")
        self.lblError.place(relx = 0.5, y= 335, anchor="center")


        # Confirmar
        frameConfirmar = tk.Frame(frameComic, bg="#1f1f1f", width=700, height=350)
        frameConfirmar.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        tk.Label(frameConfirmar, text= "Detalles:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont7).place(x=10, y= 10, anchor="nw")

        tk.Label(frameConfirmar, text= "Nombre:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(x=30, y= 75, anchor="nw")
        self.entryNombre = tk.Entry(frameConfirmar, width=15, font=controller.myFont3)
        self.entryNombre.place(x = 30, y= 100, anchor="nw")

        tk.Label(frameConfirmar, text= "Autor:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(x=300, y= 75, anchor="nw")
        self.entryAutor = tk.Entry(frameConfirmar, width=15, font=controller.myFont3)
        self.entryAutor.place(x = 300, y= 100, anchor="nw")

        tk.Label(frameConfirmar, text= "Fecha:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(x=30, y= 175, anchor="nw")
        self.entryFecha = tk.Entry(frameConfirmar, width=15, font=controller.myFont3)
        self.entryFecha.place(x = 30, y= 200, anchor="nw")

        tk.Label(frameConfirmar, text= "Descripción:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(x=300, y= 175, anchor="nw")
        self.entryDescripcion = tk.Entry(frameConfirmar, width=15, font=controller.myFont3)
        self.entryDescripcion.place(x = 300, y= 200, anchor="nw")

        btnConfirmar = tk.Button(frameConfirmar, text="Confirmar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.confirmar())
        btnConfirmar.place(relx=0.5, y= 300, anchor="center")

        self.lblError2 = tk.Label(frameConfirmar, text="", font=controller.myFont4, bg="#1f1f1f", fg="#af161a", justify="center")
        self.lblError2.place(relx = 0.5, y= 335, anchor="center")


    # Pagina siguiente
    def siguientePagina(self):
        self.lblError.config(text="")
        if self.check("pag", self.pag + 1):
            self.pag += 1
            self.lblPag.config(text="Página " + str(self.pag))

            self.esc = 1
            self.lblEscena.config(text="Escena " + str(self.esc))
        else:
            self.lblError.config(text="No se puede avanzar a la siguiente pagina porque la actual no tiene dialogos")


    # Escena siguiente
    def siguienteEscena(self):
        self.lblError.config(text="")
        if self.check("esc", self.esc + 1):
            self.esc += 1
            self.lblEscena.config(text="Escena " + str(self.esc))
        else:
            self.lblError.config(text="No se puede avanzar a la siguiente escena porque la actual no tiene dialogos")


    # Pagina anterior
    def anteriorPagina(self):
        if self.pag != 1:
            self.pag -= 1
            self.lblPag.config(text="Página " + str(self.pag))

            self.esc = 1
            self.lblEscena.config(text="Escena " + str(self.esc))


    # Escena anterior
    def anteriorEscena(self):
        if self.esc != 1:
            self.esc -= 1
            self.lblEscena.config(text="Escena " + str(self.esc))


    # Chequea si es posible continuar a la pagina o escena con el numero establecido
    # E: un string y un numero
    # S: un booleano
    def check(self, tipo, num):
        if num == 1:
            return True

        elif tipo == "pag":
            for escena in self.res["escenas"]:
                if escena["pag"] == num -1 and escena["dialogos"] != []:
                    return True
            return False

        elif tipo == "esc":
            for escena in self.res["escenas"]:
                if escena["pag"] == self.pag and escena["num"] == num - 1 and escena["dialogos"] != []:
                    return True
            return False


    # Adjunta el dialogo al resultado
    # E: personaje, dialogo (strings)
    def adjuntarDialogo(self, personaje, dialogo):
        if personaje == "" or dialogo == "":
            return

        for escena in self.res["escenas"]:
            if escena["pag"] == self.pag and escena["num"] == self.esc:
                escena["dialogos"].append({"personaje": personaje, "contenido": dialogo})

                self.entryPersonaje.delete(0, "end")
                self.entryDialogo.delete(0, "end")

                return

        newEsc = {"pag": self.pag, "num": self.esc, "dialogos": [{"personaje": personaje, "contenido": dialogo}]}

        self.res["escenas"].append(newEsc)

        self.entryPersonaje.delete(0, "end")
        self.entryDialogo.delete(0, "end")


    # Crea el comic
    def confirmar(self):
        self.lblError2.config(text="", fg="#af161a")
        if self.entryNombre.get() == "" or self.entryAutor.get() == "" or self.entryFecha.get() == "" or self.entryDescripcion.get() == "":
            self.lblError2.config(text="Debe llenar todos los campos")
            return
        elif self.res["escenas"] == []:
            self.lblError2.config(text="Debe haber al menos un dialogo")
            return
        else:
            self.res["info"]["nombre"] = self.entryNombre.get()
            self.res["info"]["autor"] = self.entryAutor.get()
            self.res["info"]["fecha"] = self.entryFecha.get()
            self.res["info"]["descripcion"] = self.entryDescripcion.get()

            try:
                f = open("C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\comics\\" + self.res["info"]["nombre"] + ".txt", "x")
            except FileExistsError:
                self.lblError2.config(text="Ya existe un comic con ese nombre, favor cambiarlo")
                return

            self.entryNombre.delete(0, "end")
            self.entryAutor.delete(0, "end")
            self.entryFecha.delete(0, "end")
            self.entryDescripcion.delete(0, "end")

            self.entryPersonaje.delete(0, "end")
            self.entryDialogo.delete(0, "end")

            self.lblError2.config(text="Comic creado exitosamente", fg="#FFFFFF")

            f.write(str(self.res))
            f.close()
            self.res = {"info": {"nombre": "", "autor": "", "fecha": "", "descripcion": "", "prefijo": ""}, "escenas": [] }





class MenuEditar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#121212")

        self.controller = controller

        labelTitulo = tk.Label(self, text="Editar ", font=controller.myFont1, bg="#1f1f1f", fg="#FFFFFF")
        labelTitulo.place(x=40, y=20)

        btnAtras = tk.Button(self, text="Cerrar Sesión", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.reset("Inicio"))
        btnAtras.place(x=636, y=20)

        btnMenu = tk.Button(self, text="Regresar", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.reset("MenuTweak"))
        btnMenu.place(x= 670, y= 60)

        tk.Label(self, text= "Seleccione el comic a editar:", fg = "#FFFFFF", bg="#121212", font=controller.myFont7).place(relx=0.5, y= 100, anchor="center")

        self.selComic = ttk.Combobox(self, state="readonly", width=50, font=controller.myFont3, values=self.getComics())
        self.selComic.place(relx=0.5, y= 150, anchor="center")
        self.selComic.bind("<<ComboboxSelected>>", lambda x: self.comicSeleccionado(x))

        frameGeneral = tk.Frame(self, bg="#121212", width=700, height=700)
        frameGeneral.place(relx=0.5, rely=0.6, anchor="center")
        frameGeneral.grid_propagate(False)

        tk.Button(self, text = "Update", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.update()).place(relx=0.9, y= 140, anchor="center")

        # Selector
        frameSelector = tk.Frame(frameGeneral, bg="#1f1f1f", width=690, height=150)
        frameSelector.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        tk.Label(frameSelector, text= "Seleccionar:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont10).place(relx=0.5, y= 10, anchor="center")

        tk.Label(frameSelector, text= "Pagina:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(relx=0.2, y= 40, anchor="center")
        self.selPagSelector = ttk.Combobox(frameSelector, state="readonly", width=20, font=controller.myFont3, values=[])
        self.selPagSelector.place(relx=0.5, y= 40, anchor="center")
        self.selPagSelector.bind("<<ComboboxSelected>>", lambda x: self.obtenerEscenas(x))

        tk.Label(frameSelector, text= "Escena:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(relx=0.2, y= 75, anchor="center")
        self.selEscSelector = ttk.Combobox(frameSelector, state="readonly", width=20, font=controller.myFont3, values=[])
        self.selEscSelector.place(relx=0.5, y= 75, anchor="center")
        self.selEscSelector.bind("<<ComboboxSelected>>", lambda x: self.obtenerDialogos(x))

        tk.Label(frameSelector, text= "Dialogo:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(relx=0.2, y= 110, anchor="center")
        self.selDiaSelector = ttk.Combobox(frameSelector, state="readonly", width=20, font=controller.myFont3, values=[])
        self.selDiaSelector.place(relx=0.5, y= 110, anchor="center")

        # Eliminar
        frameEliminar = tk.Frame(frameGeneral, bg="#1f1f1f", width=690, height=150)
        frameEliminar.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        tk.Label(frameEliminar, text= "Eliminar:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont10).place(relx=0.5, y= 15, anchor="center")

        tk.Button(frameEliminar, text="Eliminar\n Comic", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.eliminarComic()).place(relx=0.2, y= 60, anchor="center")

        tk.Button(frameEliminar, text="Eliminar\n Pagina", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.eliminarPagina()).place(relx=0.4, y= 60, anchor="center")

        tk.Button(frameEliminar, text="Eliminar\n Escena", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.eliminarEscena()).place(relx=0.6, y= 60, anchor="center")

        tk.Button(frameEliminar, text="Eliminar\n Dialogo", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.eliminarDialogo()).place(relx=0.8, y= 60, anchor="center")

        self.lblEliminarError =  tk.Label(frameEliminar, text="", font=controller.myFont4, bg="#1f1f1f", fg="#af161a", justify="center")
        self.lblEliminarError.place(relx=0.5, y= 110, anchor="center")

        # Dialogos
        frameDialogos = tk.Frame(frameGeneral, bg="#1f1f1f", width=690, height=200)
        frameDialogos.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        tk.Label(frameDialogos, text= "Editar:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont10).place(relx=0.5, y= 15, anchor="center")

        tk.Label(frameDialogos, text= "Personaje:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(relx=0.2, y= 50, anchor="center")
        self.entryPersonaje = tk.Entry(frameDialogos, width=10, font=controller.myFont3)
        self.entryPersonaje.place(relx=0.2, y= 75, anchor="center")

        tk.Label(frameDialogos, text= "Diálogo:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(relx=0.6, y= 50, anchor="center")
        self.entryDialogo = tk.Entry(frameDialogos, width=40, font=controller.myFont3)
        self.entryDialogo.place(relx=0.6, y= 75, anchor="center")

        tk.Button(frameDialogos, text="Cambiar Personaje", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.editarPersonaje()).place(relx=0.3, y= 125, anchor="center")

        tk.Button(frameDialogos, text="Cambiar Diálogo", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.editarDialogo()).place(relx=0.7, y= 125, anchor="center")

        self.lblDialogoError = tk.Label(frameDialogos, text="", font=controller.myFont4, bg="#1f1f1f", fg="#af161a", justify="center")
        self.lblDialogoError.place(relx=0.5, y= 175, anchor="center")

        # Orden
        frameOrden = tk.Frame(frameGeneral, bg="#1f1f1f", width=690, height=160)
        frameOrden.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        tk.Label(frameOrden, text= "Orden:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont10).place(relx=0.5, y= 15, anchor="center")

            # Dialogo
        tk.Label(frameOrden, text= "Dialogo:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(relx=0.2, y= 20, anchor="center")

        tk.Label(frameOrden, text= "Elija el dialogo a mover", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont8).place(relx=0.2, y= 40, anchor="center")
        self.selDia1 = ttk.Combobox(frameOrden, state="readonly", width=20, font=controller.myFont3, values=[])
        self.selDia1.place(relx=0.2, y= 65, anchor="center")

        tk.Label(frameOrden, text= "Elija el dialogo con el cual se va a cambiar", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont8).place(relx=0.2, y= 100, anchor="center")
        self.selDia2 = ttk.Combobox(frameOrden, state="readonly", width=20, font=controller.myFont3, values=[])
        self.selDia2.place(relx=0.2, y= 125, anchor="center")

            # Escena
        tk.Label(frameOrden, text= "Escena:", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont4).place(relx=0.8, y= 20, anchor="center")

        tk.Label(frameOrden, text= "Elija la escena a mover", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont8).place(relx=0.8, y= 40, anchor="center")
        self.selEsc1 = ttk.Combobox(frameOrden, state="readonly", width=20, font=controller.myFont3, values=[])
        self.selEsc1.place(relx=0.8, y= 65, anchor="center")

        tk.Label(frameOrden, text= "Elija la escena con la cual se va a cambiar", fg = "#FFFFFF", bg="#1f1f1f", font=controller.myFont8).place(relx=0.8, y= 100, anchor="center")
        self.selEsc2 = ttk.Combobox(frameOrden, state="readonly", width=20, font=controller.myFont3, values=[])
        self.selEsc2.place(relx=0.8, y= 125, anchor="center")

        tk.Button(frameOrden, text="Cambiar Dialogo", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.cambiarDialogo()).place(relx=0.5, y= 50, anchor="center")

        tk.Button(frameOrden, text="Cambiar Escena", font=controller.myFont3, bg="#1f1f1f", fg="#FFFFFF", command=lambda: self.cambiarEscena()).place(relx=0.5, y= 100, anchor="center")

        self.lblOrdenError = tk.Label(frameOrden, text="", font=controller.myFont8, bg="#1f1f1f", fg="#af161a", justify="center")
        self.lblOrdenError.place(relx=0.5, rely=0.9, anchor="center")


    # Cambiar dos escenas
    def cambiarEscena(self):
        global contents
        if self.selEsc1.get() == "" or self.selEsc2.get() == "":
            self.lblOrdenError.config(text="No se han seleccionado las escenas")
            return
        else:
            pag = self.selPagSelector.get()[-1]
            esc1 = self.selEsc1.get()[-1]
            esc2 = self.selEsc2.get()[-1]
            for escena in contents["escenas"]:
                if escena["pag"] == int(pag) and escena["num"] == int(esc1):
                    escena["num"] = int(esc2)
                elif escena["pag"] == int(pag) and escena["num"] == int(esc2):
                    escena["num"] = int(esc1)

        f = comicFile(self.selComic.get())
        f.contenido = str(contents)
        f.escribir()

        self.lblOrdenError.config(text="Escenas cambiados exitosamente")
        self.resetSelectores()
        self.selEsc1.set("")
        self.selEsc2.set("")


    # Cambia dos dialogos
    def cambiarDialogo(self):
        global contents
        if self.selDia1.get() == "" or self.selDia2.get() == "":
            self.lblOrdenError.config(text="No se han seleccionado los dialogos")
            return
        else:
            pag = self.selPagSelector.get()[-1]
            esc = self.selEscSelector.get()[-1]
            for escena in contents["escenas"]:
                if escena["pag"] == int(pag) and escena["num"] == int(esc):
                    for dialogo in escena["dialogos"]:
                        if dialogo["personaje"] + ": " + dialogo["contenido"] == self.selDia1.get():
                            dialogo["personaje"] = self.selDia2.get().split(": ")[0]
                            dialogo["contenido"] = self.selDia2.get().split(": ")[1]
                        elif dialogo["personaje"] + ": " + dialogo["contenido"] == self.selDia2.get():
                            dialogo["personaje"] = self.selDia1.get().split(": ")[0]
                            dialogo["contenido"] = self.selDia1.get().split(": ")[1]

        f = comicFile(self.selComic.get())
        f.contenido = str(contents)
        f.escribir()

        self.lblOrdenError.config(text="Dialogos cambiados exitosamente")
        self.resetSelectores()
        self.selDia1.set("")
        self.selDia2.set("")


    # Editar Personaje
    def editarPersonaje(self):
        global contents
        if self.entryPersonaje == "" or self.selDiaSelector.get() == "":
            self.lblDialogoError.config(text="No se ha seleccionado un dialogo o no se ha escrito un personaje")
            return
        else:
            pag = self.selPagSelector.get()[-1]
            esc = self.selEscSelector.get()[-1]
            dia = self.selDiaSelector.get()
            for escena in contents["escenas"]:
                if escena["pag"] == int(pag) and escena["num"] == int(esc):
                    for dialogo in escena["dialogos"]:
                        if dialogo["personaje"] + ": " + dialogo["contenido"] == dia:
                            dialogo["personaje"] = self.entryPersonaje.get()

        f = comicFile(self.selComic.get())
        f.contenido = str(contents)
        f.escribir()
        self.resetSelectores()
        self.entryPersonaje.delete(0, "end")

        self.lblDialogoError.config(text="Personaje cambiado exitosamente")


    # Editar Dialogo
    def editarDialogo(self):
        global contents
        if self.entryDialogo == "" or self.selDiaSelector.get() == "":
            self.lblDialogoError.config(text="No se ha seleccionado un dialogo o no se ha escrito")
            return
        else:
            pag = self.selPagSelector.get()[-1]
            esc = self.selEscSelector.get()[-1]
            dia = self.selDiaSelector.get()
            for escena in contents["escenas"]:
                if escena["pag"] == int(pag) and escena["num"] == int(esc):
                    for dialogo in escena["dialogos"]:
                        if dialogo["personaje"] + ": " + dialogo["contenido"] == dia:
                            dialogo["contenido"] = self.entryDialogo.get()

        f = comicFile(self.selComic.get())
        f.contenido = str(contents)
        f.escribir()
        self.resetSelectores()
        self.entryDialogo.delete(0, "end")

        self.lblDialogoError.config(text="Dialogo cambiado exitosamente")


    # Elimina un comic
    def eliminarComic(self):
        if self.selComic.get() == "":
            self.lblEliminarError.config(text="No se ha seleccionado un comic")
            return
        file = self.selComic.get() + ".txt"
        loc = "C:\\Users\\User\\OneDrive\\TallerProgramacion\\Proyecto 3\\comics"
        path = os.path.join(loc, file)
        os.remove(path)

        self.resetSelectores()
        self.selComic.set("")
        self.selComic.config(values=self.getComics())

        self.lblEliminarError.config(text="Comic eliminado exitosamente")


    # Elimina una pagina
    def eliminarPagina(self):
        global contents
        if self.selPagSelector.get() == "":
            self.lblEliminarError.config(text="No se ha seleccionado una pagina")
            return
        elif len(self.getPaginas()) == 1:
            self.lblEliminarError.config(text="No se puede eliminar la unica pagina. Intente eliminar el comic completo")
            return
        else:
            pag = self.selPagSelector.get()[-1]
            for escena in contents["escenas"]:
                if escena["pag"] == int(pag):
                    contents["escenas"].remove(escena)
                elif escena["pag"] > int(pag):
                    escena["pag"] -= 1

        f = comicFile(self.selComic.get())
        f.contenido = str(contents)
        f.escribir()
        self.resetSelectores()

        self.lblEliminarError.config(text="Pagina eliminada exitosamente")


    # Elimina una escena
    def eliminarEscena(self):
        global contents
        if self.selEscSelector.get() == "":
            self.lblEliminarError.config(text="No se ha seleccionado una escena")
            return
        elif len(self.getEscenas()) == 1:
            self.lblEliminarError.config(text="No se puede eliminar la unica escena. Intente eliminar la pagina completa")
            return
        else:
            pag = self.selPagSelector.get()[-1]
            esc = self.selEscSelector.get()[-1]
            for escena in contents["escenas"]:
                if escena["pag"] == int(pag) and escena["num"] == int(esc):
                    contents["escenas"].remove(escena)
                elif escena["pag"] == int(pag) and escena("num") > int(esc):
                    escena["num"] -= 1

        f = comicFile(self.selComic.get())
        f.contenido = str(contents)
        f.escribir()
        self.resetSelectores()

        self.lblEliminarError.config(text="Escena eliminada exitosamente")


    # Elimina un dialogo
    def eliminarDialogo(self):
        global contents
        if self.selDiaSelector.get() == "":
            self.lblEliminarError.config(text="No se ha seleccionado un dialogo")
            return
        elif len(self.getDialogos()) == 1:
            self.lblEliminarError.config(text="No se puede eliminar el unico dialogo. Intente eliminar la escena completa o cambiar este dialogo")
            return
        else:
            pag = self.selPagSelector.get()[-1]
            esc = self.selEscSelector.get()[-1]
            dia = self.selDiaSelector.get()
            for escena in contents["escenas"]:
                if escena["pag"] == int(pag) and escena["num"] == int(esc):
                    for dialogo in escena["dialogos"]:
                        if dialogo["personaje"] + ": " + dialogo["contenido"] == dia:
                            escena["dialogos"].remove(dialogo)
        f = comicFile(self.selComic.get())
        f.contenido = str(contents)
        f.escribir()
        self.resetSelectores()

        self.lblEliminarError.config(text="Dialogo eliminado exitosamente")


    # Pone los selectores en blanco
    def resetSelectores(self):
        self.selPagSelector.set("")
        self.selEscSelector.set("")
        self.selDiaSelector.set("")
        self.selPagSelector.config(values=[])
        self.selEscSelector.config(values=[])
        self.selDiaSelector.config(values=[])


    # Updatea los slects de acuerdo al comic seleccionado
    def comicSeleccionado(self, event=None):
        self.getContents(self.selComic.get())
        self.selPagSelector.config(values=self.getPaginas())
        self.selPagSelector.set("")
        self.selEscSelector.set("")
        self.selEscSelector.config(values=[])
        self.selDiaSelector.set("")
        self.selDiaSelector.config(values=[])


    # Obtiene el contenido de un comic
    def getContents(self, comic):
        global contents
        f = comicFile(comic)
        contents = f.contenido
        contents = eval(contents)


    # Obtiene las paginas de un comic
    # S: una lista de strings
    def getPaginas(self):
        global contents
        res = []
        for escena in contents["escenas"]:
            pag = "Pagina " + str(escena["pag"])
            if pag not in res:
                res.append(pag)
        return res


    # Obtiene las escenas de una página
    # S: una lista de strings
    def getEscenas(self):
        global contents
        pag = self.selPagSelector.get()[-1]
        res = []
        for escena in contents["escenas"]:
            if escena["pag"] == int(pag):
                res.append("Escena " + str(escena["num"]))
        return res


    # Coloca las escenas en el selector
    def obtenerEscenas(self, event=None):
        res = self.getEscenas()
        self.selEscSelector.config(values=res)
        self.selEsc1.config(values=res)
        self.selEsc2.config(values=res)


    # Obtiene los dialogos de una escena
    # S: una lista de strings
    def getDialogos(self):
        global contents
        pag = self.selPagSelector.get()[-1]
        esc = self.selEscSelector.get()[-1]
        res = []

        for escena in contents["escenas"]:
            if escena["pag"] == int(pag) and escena["num"] == int(esc):
                for dialogo in escena["dialogos"]:
                    text = dialogo["personaje"] + ": " + dialogo["contenido"]
                    res.append(text)
        return res


    # Updatea los comics del selector
    def update(self):
        self.selComic.config(values=self.getComics())

    # Coloca los dialogos en el selector
    def obtenerDialogos(self, event=None):
        res = self.getDialogos()
        self.selDiaSelector.config(values=res)
        self.selDia1.config(values=res)
        self.selDia2.config(values=res)


    # Obtiene los comics en el folder
    def getComics(self):
        directory = 'Proyecto 3\\comics'
        res = []

        files = Path(directory).glob('*')
        for file in files:
            filename = Path(file).stem
            res.append(filename)

        return res


    # Resetea la ventana
    def reset(self, frame):
        global contents
        self.selComic.set("")
        self.selPagSelector.config(values=[])
        self.selPagSelector.set("")
        self.selEscSelector.config(values=[])
        self.selEscSelector.set("")
        self.selDiaSelector.config(values=[])
        self.selDiaSelector.set("")
        contents = []
        self.controller.showFrame(frame)



app = main()
app.mainloop()
