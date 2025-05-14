import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector

class App:
    def __init__(self):
        # Configuración inicial de la ventana principal
        self.root = ttk.Window(themename="cosmo")
        self.root.title("Biblioteca - Lista de Libros")
        self.root.geometry("800x600")

        # Creamos una lista vacía que almacenará todos los libros
        # Esta lista será una lista de tuplas, donde cada tupla representa un libro
        # Ejemplo: [(1, 'Don Quijote', 'Cervantes', 1605), (2, 'El Principito', 'Saint-Exupéry', 1943)]
        self.lista_libros = []

        # Creamos el contenedor principal de la aplicación
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=BOTH, expand=YES)

        # Etiqueta con el título de la aplicación
        self.title_label = ttk.Label(
            self.main_frame,
            text="Lista de Libros",
            font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(pady=10)

        # Frame que contendrá la tabla y la barra de desplazamiento
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(fill=BOTH, expand=YES)

        # Creamos la tabla (Treeview) que mostrará los libros
        # columns: Define las columnas que tendrá la tabla
        # show="headings": Muestra solo las cabeceras de las columnas
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("ID", "Titulo", "Autor", "Año"),
            show="headings"
        )

        # Configuramos las cabeceras de cada columna
        self.tree.heading("ID", text="ID")
        self.tree.heading("Titulo", text="Título")
        self.tree.heading("Autor", text="Autor")
        self.tree.heading("Año", text="Año")

        # Definimos el ancho de cada columna
        self.tree.column("ID", width=50)
        self.tree.column("Titulo", width=300)
        self.tree.column("Autor", width=200)
        self.tree.column("Año", width=100)

        # Creamos la barra de desplazamiento vertical
        self.scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient=VERTICAL,
            command=self.tree.yview
        )

        # Conectamos la barra de desplazamiento con la tabla
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Colocamos la tabla y la barra de desplazamiento en el frame
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Botón que activará la visualización de la lista de libros
        self.btn_mostrar = ttk.Button(
            self.main_frame,
            text="Mostrar Lista de Libros",
            command=self.mostrar_lista_libros,
            style="primary.TButton"
        )
        self.btn_mostrar.pack(pady=10)

        # Cargamos los datos de la base de datos al iniciar la aplicación
        self.cargar_libros()

    def conectar_db(self):
        """
        Establece la conexión con la base de datos MySQL
        """
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crud_ttklibro"
        )

    def cargar_libros(self):
        """
        Carga los libros desde la base de datos y los almacena en la lista.
        """
        conexion = self.conectar_db()
        cursor = conexion.cursor()

        # Ejecutamos la consulta SQL para obtener todos los libros
        cursor.execute("SELECT * FROM libros")

        # Guardamos los resultados en la lista
        self.lista_libros = cursor.fetchall()
        print(f"Libros cargados: {len(self.lista_libros)}")

        # Cerramos la conexión
        cursor.close()
        conexion.close()

    def mostrar_lista_libros(self):
        """
        Muestra los libros almacenados en la lista en la tabla.
        """
        # Limpiamos la tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Mostramos cada libro de la lista
        for libro in self.lista_libros:
            print(f"Mostrando libro: {libro}")
            self.tree.insert("", END, values=libro)

    def run(self):
        """
        Inicia el bucle principal de la aplicación
        """
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()