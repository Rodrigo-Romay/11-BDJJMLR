import customtkinter as ctk
from tkinter import messagebox, Toplevel, IntVar


class Columns():

    def __init__(self, root, data_table, input_columns_label, output_column_label, create_model_button):
        self.root = root
        self.data_table = data_table
        self.input_columns_label = input_columns_label
        self.output_column_label = output_column_label
        self.column_vars = {}
        self.columns_selected = []
        self.output_column = None
        self.create_model_button = create_model_button

    def select_columns(self):
        # Crear una nueva ventana para seleccionar las columnas
        self.column_window = Toplevel(self.root)
        self.column_window.title("Select Columns")
        self.column_window.resizable(False, False)
        self.column_window.configure(bg="#dfe6e9")  # Fondo azul claro suave

        # Frame para el título con fondo azul oscuro
        title_frame = ctk.CTkFrame(
            self.column_window,
            fg_color="#2c3e50",  # Azul oscuro
            corner_radius=0
        )
        title_frame.pack(fill="x", pady=(10, 5), padx=0)  # Espaciado ajustado

        title_label = ctk.CTkLabel(
            title_frame,
            text="Select Input Columns",
            text_color="#ecf0f1",  # Texto claro
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=5)

        # Frame para las opciones con fondo aún más claro
        options_frame = ctk.CTkFrame(
            self.column_window,
            fg_color="#f1f2f6",  # Azul claro pálido
            corner_radius=10
        )
        options_frame.pack(pady=(5, 5), padx=10, fill="both", expand=True)

        # Crear checkboxes dentro del frame de opciones
        self.column_vars = {}
        for col in self.data_table["columns"]:
            var = IntVar()
            if col in self.columns_selected:
                var.set(1)  # Marcar como seleccionada
            self.column_vars[col] = var

            checkbox = ctk.CTkCheckBox(
                options_frame,
                text=col,
                variable=var,
                text_color="#2c3e50",  # Texto azul oscuro
                fg_color="#3498db",  # Azul vibrante para las casillas seleccionadas
                border_color="#7f8c8d",  # Gris oscuro
                hover_color="#2980b9"  # Azul más intenso al pasar el cursor
            )
            checkbox.pack(anchor="w", padx=15, pady=2)  # Espaciado ajustado

        # Frame para los botones con fondo igual al fondo general
        button_frame = ctk.CTkFrame(
            self.column_window,
            fg_color="#dfe6e9"  # Fondo azul claro suave
        )
        button_frame.pack(pady=(5, 10))  # Espaciado compacto con el frame superior

        confirm_button = ctk.CTkButton(
            button_frame,
            text="Confirm Selection",
            command=self.confirm_selection,
            fg_color="#2ecc71",  # Verde suave para confirmar
            hover_color="#27ae60",
            text_color="white",
            font=("Helvetica", 13),
            width=160  # Botón más estrecho
        )
        confirm_button.pack(pady=3)  # Espaciado compacto entre botones

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.column_window.destroy,
            fg_color="#e74c3c",  # Rojo suave para cancelar
            hover_color="#c0392b",
            text_color="white",
            font=("Helvetica", 13),
            width=160
        )
        cancel_button.pack(pady=3)

        # Ajustar tamaño automáticamente según contenido
        self.column_window.update_idletasks()
        width = self.column_window.winfo_reqwidth() + 20
        height = self.column_window.winfo_reqheight() + 20
        self.column_window.geometry(f"{width}x{height}")

    def confirm_selection(self):
        # Obtener las columnas seleccionadas
        self.columns_selected = [
            col for col, var in self.column_vars.items() if var.get() == 1
        ]

        if self.columns_selected:
            # Actualizar la etiqueta con las columnas seleccionadas
            self.input_columns_label.configure(
                text=f"Input Columns: {', '.join(self.columns_selected)}"
            )
            self.column_window.destroy()

            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Columns Selected",
                f"Selected columns: {', '.join(self.columns_selected)}"
            )
        else:
            # Mostrar advertencia si no se seleccionó ninguna columna
            messagebox.showwarning(
                "No Selection",
                "No columns selected."
            )

    def select_output_column(self):
        # Crear una nueva ventana para seleccionar la columna de salida
        self.output_column_window = Toplevel(self.root)
        self.output_column_window.title("Select Output Column")
        self.output_column_window.resizable(False, False)
        self.output_column_window.configure(bg="#dfe6e9")  # Fondo azul claro suave

        # Frame para el título con fondo azul oscuro
        title_frame = ctk.CTkFrame(
            self.output_column_window,
            fg_color="#2c3e50",  # Azul oscuro
            corner_radius=0
        )
        title_frame.pack(fill="x", pady=(10, 5), padx=0)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Select Output Column",
            text_color="#ecf0f1",  # Texto claro
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=5)

        # Frame para las opciones con fondo más claro
        options_frame = ctk.CTkFrame(
            self.output_column_window,
            fg_color="#f1f2f6",  # Azul claro pálido
            corner_radius=10
        )
        options_frame.pack(pady=(5, 5), padx=10, fill="both", expand=True)

        # Variable para almacenar la selección de columna de salida
        self.output_column_var = ctk.StringVar(value="")  # Almacena la columna seleccionada

        # Crear radiobuttons dentro del frame de opciones
        for col in self.data_table["columns"]:
            radiobutton = ctk.CTkRadioButton(
                    options_frame,
                    text=col,
                    variable=self.output_column_var,
                    value=col,  # Cada radiobutton tiene un valor único (la columna)
                    text_color="#2c3e50",  # Texto azul oscuro
                    fg_color="#3498db",  # Gris claro por defecto
                    hover_color="#2980b9", 
                    border_color="#bdc3c7",  # Azul claro para el borde seleccionado
                    border_width_checked=4  # Borde más grueso cuando está seleccionado
                )
            radiobutton.pack(anchor="w", padx=15, pady=3)

            # Si ya hay una columna de salida seleccionada, marcarla
            if col == self.output_column:
                self.output_column_var.set(col)

        # Frame para los botones con fondo igual al fondo general
        button_frame = ctk.CTkFrame(
            self.output_column_window,
            fg_color="#dfe6e9"  # Fondo azul claro suave
        )
        button_frame.pack(pady=(5, 10))

        # Botón para confirmar selección
        confirm_button = ctk.CTkButton(
            button_frame,
            text="Confirm Selection",
            command=self.confirm_output_column,
            fg_color="#2ecc71",  # Verde suave para confirmar
            hover_color="#27ae60",
            text_color="white",
            font=("Helvetica", 13),
            width=160  # Botón más estrecho
        )
        confirm_button.pack(pady=3)

        # Botón para cancelar selección
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.output_column_window.destroy,
            fg_color="#e74c3c",  # Rojo suave para cancelar
            hover_color="#c0392b",
            text_color="white",
            font=("Helvetica", 13),
            width=160
        )
        cancel_button.pack(pady=3)

        # Ajustar tamaño automáticamente según contenido
        self.output_column_window.update_idletasks()
        width = self.output_column_window.winfo_reqwidth() + 20
        height = self.output_column_window.winfo_reqheight() + 20
        self.output_column_window.geometry(f"{width}x{height}")


    def confirm_output_column(self):
        # Obtener la columna seleccionada
        selected_output_column = self.output_column_var.get()
        if selected_output_column:
            messagebox.showinfo(
                "Output Column Selected",
                f"Selected Output Column: {selected_output_column}"
            )
            # Almacenar la columna seleccionada como atributo de clase
            self.output_column = selected_output_column
            self.output_column_window.destroy()
            self.output_column_label.configure(
                text=f"Output Column: {self.output_column}"
            )
            self.create_model_button.configure(state="normal")
        else:
            messagebox.showwarning(
                "No Column Selected",
                "Please select an output column."
            )


