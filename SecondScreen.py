from tkinter import *
from PIL import Image, ImageTk 
from funciones import crear, borrar, abrir, actualizar
from tkinter import filedialog,messagebox


class SecondScreen:
    def __init__(self):
        #Creacion y configuracion de la raiz
        self.root=Tk()
        self.root.geometry('1200x900')
        self.root.title('Recursos Humanos')
        self.root.resizable(False,False)
        self.root.config(bg='#082d44') 
        
        try:
            self.archivo=filedialog.askopenfilename(initialdir="/", title="Selecciona la base de datos", filetypes=(("Bases de datos", "*.db"), ("all files", "*.*")))
            if self.archivo[-3:] != '.db':
                messagebox.showerror('Alerta','No se selecionó una base de datos correcta')
                self.root.destroy()
                return
        except Exception as e:
            messagebox.showerror('Error',e)
        
        #Frame donde se mostraran los datos
        self.frameMostrar=Frame(self.root, bg='#082d44', borderwidth=0,highlightthickness=0)
        self.frameMostrar.place(
            height=770,
            width=1100,
            x=50,
            y=130)
        self.frameMostrar.grid_rowconfigure(0,weight=1)
        self.frameMostrar.grid_columnconfigure(0,weight=1)

        #Importar cada imagen para cada boton
        try:
            img_boton_crear=Image.open('Crear.png')
            self.photoCrear= ImageTk.PhotoImage(img_boton_crear)

            img_boton_abrir=Image.open('Abrir.png')
            self.photoAbrir=ImageTk.PhotoImage(img_boton_abrir)            

            img_boton_actualizar=Image.open('Actualizar.png') 
            self.photoActualizar=ImageTk.PhotoImage(img_boton_actualizar )

            img_boton_borrar=Image.open('Borrar.png')
            self.photoBorrar=ImageTk.PhotoImage(img_boton_borrar)

        #Creacion y configuracion de cada boton
            self.botonCrear=Button(
                image=self.photoCrear,
                cursor='hand',
                command= lambda:crear(self.archivo),
                borderwidth=0,
                highlightthickness=0
            )
            
            self.botonCrear.place(
                height=40,
                width=95,
                x=10,
                y=20,                
            )

            self.botonAbrir=Button(
                image=self.photoAbrir,
                cursor='hand',
                command=lambda:abrir(self.frameMostrar,self.archivo),
                borderwidth=0,
                highlightthickness=0
            )

            self.botonAbrir.place(
                height=40,
                width=95,
                x=130,
                y=20
            )         

            self.botonActualizar=Button(
                image=self.photoActualizar,
                cursor='hand',
                command=lambda:actualizar(self.archivo),
                borderwidth=0,
                highlightthickness=0
            )

            self.botonActualizar.place(
                height=30,
                width=145,
                x=250,
                y=23
            )

            self.botonBorrar=Button(
                image=self.photoBorrar,
                cursor='hand',
                command=lambda:borrar(self.archivo),
                borderwidth=0,
                highlightthickness=0
            )

            self.botonBorrar.place(
                height=40,
                width=110,
                x=430,
                y=21

            )

        except Exception as e:
            print(e)

        self.root.mainloop()
