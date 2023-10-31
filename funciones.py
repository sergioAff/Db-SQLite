import sqlite3 as sql
from tkinter import messagebox, simpledialog, NONE, END, DISABLED
from tkinter import *

def crear(archivo):
    nombreTabla = simpledialog.askstring('Nombre de la tabla', 'Introduce el nombre de la tabla: ', initialvalue='NoName')
    if not nombreTabla:
        messagebox.showerror('Aviso', 'No se proporcionó el nombre de la tabla')
        return

    atributos = []
    conn = sql.connect(archivo)
    cursor = conn.cursor()

    primaryKey = 'no'

        # Solicitar al usuario que introduzca los atributos de la tabla
    while True:
        nombreAtributo = simpledialog.askstring('Nombre del atributo', 'Introduce el nombre del nuevo atributo (o deja en blanco para finalizar):')
        if not nombreAtributo:
             break

        while True:
            tipoDato = simpledialog.askstring('Tipo de dato', f'Introduce el tipo de dato para "{nombreAtributo}" (1-texto, 2-numero entero, 3-numero decimal):')
            if tipoDato.lower() == '1' or tipoDato.lower() == '2' or tipoDato.lower() == '3':
                if tipoDato.lower() == '1':
                    tipoDato = 'TEXT'
                elif tipoDato.lower() == '2':
                    tipoDato = 'INTEGER'
                elif tipoDato.lower() == '3':
                    tipoDato = 'REAL'
                break
            else:
                continue

            # Preguntar al usuario si desea definir el atributo como clave primaria
        if primaryKey == 'no':
            while True:
                esClavePrimaria = simpledialog.askstring('Clave primaria', f'¿El atributo "{nombreAtributo}" es una clave primaria? (Sí/No):')
                if esClavePrimaria.lower() == 'si' or esClavePrimaria.lower() == 'sí':
                    while True:
                        if tipoDato == 'INTEGER':
                            autoincrement = simpledialog.askstring('Autoincrementable', f'¿Quieres que la llave primaria {nombreAtributo} sea autoincrementable? (Sí/No):')
                            if autoincrement.lower() == 'no':
                                atributos.append(f'{nombreAtributo} {tipoDato} PRIMARY KEY')
                            elif autoincrement.lower() == 'si':
                                atributos.append(f'{nombreAtributo} {tipoDato} PRIMARY KEY AUTOINCREMENT')
                            else:
                                continue
                        else:
                            atributos.append(f'{nombreAtributo} {tipoDato} PRIMARY KEY')

                        primaryKey = 'si'
                        break
                elif esClavePrimaria.lower() == 'no':
                    atributos.append(f'{nombreAtributo} {tipoDato}')
                    break
                else:
                    continue
                break
                
        else:
            atributos.append(f'{nombreAtributo} {tipoDato}')
                
        # Crear la tabla con los atributos proporcionados por el usuario
    if atributos:
        atributosDefinicion = ', '.join(atributos)
        create_table_query = f'''CREATE TABLE IF NOT EXISTS {nombreTabla}(
                                    {atributosDefinicion}
                                    )'''
        cursor.execute(create_table_query)

            # Preguntar al usuario si desea agregar una clave externa
        esClaveExterna = simpledialog.askstring('Clave externa', '¿Deseas agregar una foregin key a esta tabla? (Sí/No):')
        if esClaveExterna.lower() == 'si':
            nombreTablaReferencia = simpledialog.askstring('Tabla de referencia', 'Introduce el nombre de la tabla de referencia:')
            nombreClaveReferencia = simpledialog.askstring('Columna de referencia', 'Introduce el nombre de la clave de referencia:')
            try:
                cursor.execute(f'FOREIGN KEY ({nombreClaveReferencia}) REFERENCES {nombreTablaReferencia}({nombreClaveReferencia})')
            except Exception as e:
                messagebox.showerror(str(e))
                print(e)
        conn.commit()
    else:
        messagebox.showinfo('Aviso', "No se creó la tabla porque no se proporcionaron atributos.")

    conn.close()

def borrar(archivo):
        # Crear una ventana
    ventana = Toplevel()
    ventana.title("Eliminar Atributo o Tabla")

        # Función para manejar el botón Eliminar
    def eliminar():
        tipo = tipo_entry.get().lower()
        nombre = nombre_entry.get()

            # Conectar a la base de datos
        conn = sql.connect(archivo)
        cursor = conn.cursor()

            # Verificar si el tipo es "atributo"
        if tipo == 'atributo':
                # Solicitar el nombre de la tabla
            tabla = tabla_entry.get()

                # Verificar si la tabla existe
            cursor.execute(f"PRAGMA table_info({tabla})")
            if cursor.fetchall():
                    # Verificar si el atributo existe en la tabla
                cursor.execute(f"PRAGMA table_info({tabla})")
                columnas = [column[1] for column in cursor.fetchall()]
                if nombre in columnas:
                        # Eliminar las referencias de clave externa primero
                    cursor.execute(f"PRAGMA foreign_key_list({tabla})")
                    foreign_keys = cursor.fetchall()
                    for fk in foreign_keys:
                        if fk[3] == nombre:
                            cursor.execute(f"ALTER TABLE {tabla} DROP CONSTRAINT {fk[1]}")
                        # Luego, eliminar el atributo
                    try:
                        cursor.execute(f"ALTER TABLE {tabla} DROP COLUMN {nombre}")
                        conn.commit()
                        messagebox.showinfo("Éxito", f"El atributo '{nombre}' ha sido eliminado con éxito de la tabla '{tabla}'.")
                    except sql.OperationalError:
                        messagebox.showerror('Error', 'No se puede borrar la llave primaria')
                else:
                    messagebox.showerror("Error", f"No se encontró el atributo '{nombre}' en la tabla '{tabla}'.")
            else:
                messagebox.showerror("Error", f"No se encontró la tabla '{tabla}' en la base de datos.")
        elif tipo == 'tabla':
            cursor.execute(f"DROP TABLE IF EXISTS {nombre}")
            conn.commit()
            messagebox.showinfo("Éxito", f"La tabla '{nombre}' ha sido eliminada con éxito.")
        else:
            messagebox.showerror("Error", "Por favor, ingrese 'tabla' o 'atributo' en el campo 'Tipo'.")
            
        conn.close()
        ventana.destroy()

        # Etiqueta y entrada para el tipo (atributo o tabla)
    tipo_label = Label(ventana, text="Tipo (atributo o tabla):")
    tipo_label.pack()
    tipo_entry = Entry(ventana)
    tipo_entry.pack()

        # Etiqueta y entrada para el nombre
    nombre_label = Label(ventana, text="Nombre:")
    nombre_label.pack()
    nombre_entry = Entry(ventana)
    nombre_entry.pack()

        # Etiqueta y entrada para la tabla (solo si se ingresa "atributo")
    tabla_label = Label(ventana, text="Tabla (solo si es 'atributo'):")
    tabla_label.pack()
    tabla_entry = Entry(ventana)
    tabla_entry.pack()

        # Botón para eliminar
    eliminar_button = Button(ventana, text="Eliminar", command=eliminar)
    eliminar_button.pack()

    ventana.mainloop()

def abrir(frameMostrar,archivo):
    
    for widget in frameMostrar.winfo_children():
        widget.destroy()

        # Solicitar el nombre de la tabla al usuario
    nombre_tabla = simpledialog.askstring('Abrir Tabla', 'Introduce el nombre de la tabla que deseas abrir:')

    tituloTabla = Label(text=f'Tabla: {nombre_tabla}', anchor='w')
    tituloTabla.config(bg='#082d44', font=(['Arial', 20]),fg='white')
    tituloTabla.place(
        height=40,
        width=500,
        x=10,
        y=80
    )

    if nombre_tabla:
            # Conectar a la base de datos
        conn = sql.connect(archivo)
        cursor = conn.cursor()

            # Verificar si la tabla existe
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nombre_tabla,))
        tabla_existe = cursor.fetchone()

        if tabla_existe:
                # Obtener los nombres de los atributos de la tabla
            cursor.execute(f"PRAGMA table_info({nombre_tabla})")
            atributos = [column[1] for column in cursor.fetchall()]

                # Obtener los valores de la tabla
            cursor.execute(f"SELECT * FROM {nombre_tabla}")
            valores = cursor.fetchall()

                # Crear un widget de texto con barras de desplazamiento automáticas
            texto = Text(frameMostrar, wrap=NONE, highlightthickness=0)
            texto.config(bg='#082d44', fg='white', font=('Arial', 20))
            texto.grid(row=0, column=0, sticky="nsew")

            scrollbar_horizontal=Scrollbar(frameMostrar,orient='horizontal')
            scrollbar_horizontal.config(command=texto.xview)
            scrollbar_horizontal.place(
                x=370,
                y=730,
                width=300
            )

            scrollbar_vertical=Scrollbar(frameMostrar,orient='vertical')
            scrollbar_vertical.config(command=texto.yview)
            scrollbar_vertical.place(
                x=1085,
                y=250,
                height=300
            )
            texto.config(xscrollcommand=scrollbar_horizontal.set, yscrollcommand=scrollbar_vertical.set)        


                # Configurar el frame para que el widget de texto se expanda automáticamente
            frameMostrar.grid_rowconfigure(0, weight=1)
            frameMostrar.grid_columnconfigure(0, weight=1)

                # Mostrar los nombres de los atributos en el widget de texto
            texto.insert(END, "\t\t\t".join(atributos))

                # Mostrar los valores de los campos alineados
            for registro in valores:
                texto.insert(END, '\n')
                texto.insert(END, '\t\t\t'.join(str(campo) for campo in registro))

                # Desactivar la edición en el widget de texto
            texto.config(state=DISABLED)
        else:
            messagebox.showerror("Error", f"No se encontró la tabla '{nombre_tabla}' en la base de datos.")

        conn.close()

def actualizar(archivo):
    nombre_tabla = simpledialog.askstring('Tabla a trabajar', 'Nombre de la tabla en la que quiere trabajar')
    if not nombre_tabla:
        messagebox.showerror('Aviso', 'No se introdujo ningún nombre para la tabla')
        return

    conn = sql.connect(archivo)
    cursor = conn.cursor()

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nombre_tabla,))
    tabla_existe = cursor.fetchone()

    if not tabla_existe:
        messagebox.showerror('Aviso', f'{nombre_tabla} no existe en la base de datos')
        conn.close()
        return

    while True:
        accion = simpledialog.askstring("Actualizar Base de Datos", "Seleccione la acción:\n\n1. Cambiar nombre de atributo\n2. Añadir atributo\n3. Borrar valor de campo\n4. Cambiar valor de campo\n5. Añadir valor de campo\n6. Añadir registro\n\nDeja en blanco para salir")
        if not accion:
            break

        if accion == "1":
            atributo_antiguo = simpledialog.askstring("Cambiar Nombre de Atributo", "Introduce el nombre del atributo que deseas cambiar:")
            if atributo_antiguo:
                atributo_nuevo = simpledialog.askstring("Cambiar Nombre de Atributo", f"Introduce el nuevo nombre para {atributo_antiguo}:")
                if atributo_nuevo:
                    cursor.execute(f"ALTER TABLE {nombre_tabla} RENAME COLUMN {atributo_antiguo} TO {atributo_nuevo}")
                    conn.commit()

        elif accion == "2":
            atributo = simpledialog.askstring("Añadir Atributo", "Introduce el nombre del nuevo atributo:")
            if atributo:
                tipoDato = simpledialog.askstring("Añadir Atributo", "Introduce el tipo de dato del nuevo atributo: (1-texto, 2-numero entero, 3-numero decimal):")
                if tipoDato.lower() == '1' or tipoDato.lower() == '2' or tipoDato.lower() == '3':
                    if tipoDato.lower() == '1':
                        tipoDato = 'text'
                    elif tipoDato.lower() == '2':
                        tipoDato = 'integer'
                    elif tipoDato.lower() == '3':
                        tipoDato = 'real'
                    cursor.execute(f"ALTER TABLE {nombre_tabla} ADD COLUMN {atributo} {tipoDato}")
                    conn.commit()

        elif accion == "3":
            campo = simpledialog.askstring("Borrar Valor de Campo", "Introduce el nombre del atributo al que pertenece el valor que quieres borrar: (Columna)")
            if campo:
                id_registro = simpledialog.askstring("Borrar Valor de Campo", "Introduce el ID del registro al que pertenece el valor que quieres borrar: (Fila)")
                if id_registro:
                    try:
                        cursor.execute(f"UPDATE {nombre_tabla} SET {campo} = ? WHERE id = ?", (None, id_registro))
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Valor del campo '{campo}' eliminado para el registro con ID {id_registro}.")
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

        elif accion == "4":
                # Solicita el nombre del atributo (campo) a modificar
            campo = simpledialog.askstring("Cambiar Valor de Campo", "Introduce el nombre del atributo (campo) al que pertenece el valor que deseas cambiar:")
            if campo:
                    # Solicita el ID del registro que deseas modificar
                id_registro = simpledialog.askstring("Cambiar Valor de Campo", "Introduce el ID del registro al que pertenece el valor que deseas cambiar:")
                if id_registro:
                        # Solicita el nuevo valor para el campo
                    nuevo_valor = simpledialog.askstring("Cambiar Valor de Campo", "Introduce el nuevo valor para el campo:")
                    if nuevo_valor is not None:
                        try:
                                # Actualiza el valor en la base de datos
                            cursor.execute(f"UPDATE {nombre_tabla} SET {campo} = ? WHERE id = ?", (nuevo_valor, int(id_registro)))
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Valor del campo '{campo}' actualizado para el registro con ID {id_registro}.")
                        except Exception as e:
                            messagebox.showerror("Error", str(e))
                    else:
                        messagebox.showerror('Alerta','No se introdujo nigun valor')
        elif accion == "5":
            campo = simpledialog.askstring("Añadir Valor de Campo", "Introduce el nombre del atributo donde se quiere añadir el valor:")
            if campo:
                nuevo_valor = simpledialog.askstring("Añadir Valor de Campo", "Introduce el valor a añadir:")
                if nuevo_valor:
                    try:
                        cursor.execute(f"INSERT INTO {nombre_tabla} ({campo}) VALUES (?)", (nuevo_valor,))
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Valor '{nuevo_valor}' añadido al campo '{campo}'.")
                    except Exception as e:
                        messagebox.showerror(f'No se encontró el atributo : {e}')

        elif accion == "6":
            cursor.execute(f"PRAGMA table_info({nombre_tabla})")
            atributos_info = cursor.fetchall()
            atributos = [column[1] for column in atributos_info]
            autoincrementable = any(col[1] == 'INTEGER' and 'autoincrement' in col[2].lower() for col in atributos_info)
    
            valores = []

            for atributo in atributos:
                valor = simpledialog.askstring("Añadir Registro", f"Introduce el valor para el atributo '{atributo}':")
                valores.append(valor)

            if not autoincrementable:
                if "id" in atributos:
                    id_index = atributos.index("id")
                    provided_id = valores[id_index]

                    if provided_id:
                        cursor.execute(f"SELECT id FROM {nombre_tabla} WHERE id = ?", (provided_id,))
                        existing_id = cursor.fetchone()
                        if existing_id:
                            messagebox.showerror("Error", "El ID proporcionado ya existe en la tabla.")
                            return

            if len(valores) == len(atributos):
                if autoincrementable and "id" not in atributos:
                        # No incluir el campo de ID en la inserción
                    atributos = atributos[1:]  # Ignorar el primer atributo (id)
                    valores = valores[1:]
            
                placeholders = ', '.join(['?' for _ in atributos])
                query = f"INSERT INTO {nombre_tabla} ({', '.join(atributos)}) VALUES ({placeholders})"
                try:
                    cursor.execute(query, valores)
                    conn.commit()
                except sql.IntegrityError as e:
                    messagebox.showerror('Alerta','Introdujo algun tipo de dato erroneo')
                    print(e)
                messagebox.showinfo("Éxito", "Registro agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se proporcionaron valores para todos los atributos.")

    conn.close()