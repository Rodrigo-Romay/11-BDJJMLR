import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, IntVar, simpledialog
from tkinter import ttk




class Columns():

    def __init__(self,root,data_table,input_columns_label,output_column_label):
        self.root = root
        self.data_table = data_table
        self.input_columns_label = input_columns_label
        self.output_column_label = output_column_label
        self.column_vars = {}
        self.columns_selected = []
        self.output_column = None


    

    def select_columns(self):
        # Crear una nueva ventana para seleccionar las columnas
        self.column_window = Toplevel(self.root)
        self.column_window.title("Select Columns")
        self.column_window.configure(bg="black")
       

        for idx, col in enumerate(self.data_table["columns"]):
            var = IntVar()
            self.column_vars[col] = var
            checkbox = ctk.CTkCheckBox(self.column_window, text=col, variable=var, text_color="white",fg_color="black")
            checkbox.pack(anchor="w")
    
        confirm_button = ctk.CTkButton(self.column_window, text="Confirm Selection", command=self.confirm_selection)
        confirm_button.pack(pady=10)
        


    def confirm_selection(self):
        self.columns_selected = [col for col, var in self.column_vars.items() if var.get() == 1]
        if self.columns_selected:
                self.input_columns_label.configure(text=f"Input Columns: {', '.join(self.columns_selected)}")
                self.column_window.destroy()
                messagebox.showinfo("Columns Selected", f"Selected columns: {', '.join(self.columns_selected)}")
        else:
            messagebox.showwarning("No Selection", "No columns selected.")
        self.column_window.destroy()


    def select_output_column(self):
        # Crear una nueva ventana para seleccionar la columna de salida
        self.output_column_window = Toplevel(self.root)
        self.output_column_window.title("Select Output Column")

        self.output_column_window.configure(bg="black")

        # Variable para almacenar la selección de columna de salida
        self.output_column_var = ctk.StringVar(value="")  # Almacena la columna seleccionada

        # Crear radiobuttons para cada columna
        for idx, col in enumerate(self.data_table["columns"]):
            radiobutton = ctk.CTkRadioButton(self.output_column_window, 
                                            text=col, 
                                            variable=self.output_column_var, 
                                            value=col,  # Cada radiobutton tiene un valor único (la columna)
                                            text_color="white",
                                            fg_color="blue",
                                            hover_color="#444444")
            radiobutton.pack(anchor="w")

        # Botón para confirmar la selección
        confirm_button = ctk.CTkButton(self.output_column_window, 
                                    text="Confirm Output Column", 
                                    command=self.confirm_output_column,
                                    fg_color="blue",
                                    text_color="white")
                                    
        confirm_button.pack(pady=10)


    def confirm_output_column(self):
        # Obtener la columna seleccionada
        self.selected_output_column = self.output_column_var.get()
        if self.selected_output_column:
            messagebox.showinfo("Output Column Selected", f"Selected Output Column: {self.selected_output_column}")
            self.output_column = self.selected_output_column  # Almacenar la columna seleccionada como atributo de clase

            self.output_column_window.destroy()
            self.output_column_label.configure(text=f"Output Column: {self.output_column}")

        else:
            messagebox.showwarning("No Column Selected", "Please select an output column.")
