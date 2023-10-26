from tkinter import *
from PIL import Image, ImageTk
from SecondScreen import SecondScreen

class Screen:
    def __init__(self):
        # Creación y configuración de la raíz
        self.root = Tk()
        self.root.geometry('1000x800')
        self.root.title('Recursos Humanos')
        self.root.resizable(True, True)  # Permite redimensionar la ventana
        self.root.config(bg='#082d44')
        self.icono = PhotoImage(file='icono.png')
        self.root.iconphoto(True, self.icono)

        # Carga de la imagen
        try:
            img_boton_comenzar = Image.open('Comenzar.png')
            self.photoBotonComenzar = ImageTk.PhotoImage(img_boton_comenzar)
        except Exception as e:
            print(e)

        # Creación del botón Comenzar
        self.botonComenzar = Button(
            image=self.photoBotonComenzar,
            command=self.comenzar,
            cursor='hand',
            borderwidth=0,
            highlightthickness=0
        )

        self.botonComenzar.place(
            height=90,
            width=290,
            x=0,
            y=0
        )

        # Centrar el botón en la ventana
        self.root.update_idletasks()  # Forzar la actualización de la geometría
        x = (self.root.winfo_width() - self.botonComenzar.winfo_reqwidth()) // 2+50
        y = (self.root.winfo_height() - self.botonComenzar.winfo_reqheight()) // 2+20
        self.botonComenzar.place(x=x, y=y)

        self.root.mainloop()

    def comenzar(self):
        self.root.destroy()
        self.secondScreen = SecondScreen()

if __name__ == "__main__":
    Screen()
