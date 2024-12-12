import customtkinter as ctk
from tkinter import messagebox, Toplevel, IntVar


#===================================== COLUMNS =====================================

class Columns():
    """Class for managing column selection for input and output in a GUI."""

    def __init__(self, root, data_table, input_columns_label, output_column_label, create_model_button,make_prediction_button):
        """
        Initialize the Columns class.

        Args:
            root (Tk): The root window of the application.
            data_table (dict): Dictionary containing data table information, including column names.
            input_columns_label (CTkLabel): Label to display selected input columns.
            output_column_label (CTkLabel): Label to display the selected output column.
            create_model_button (CTkButton): Button to trigger model creation, enabled after selection.
        """

        self.root = root
        self.data_table = data_table
        self.input_columns_label = input_columns_label
        self.output_column_label = output_column_label
        self.column_vars = {}
        self.columns_selected = []
        self.output_column = None
        self.create_model_button = create_model_button
        self.make_prediction_button = make_prediction_button

    #-------------------------------------- INPUT COLUMNS ---------------------------------

    def select_columns(self):
        """
        Open a window to allow the user to select input columns from the data table.

        The selected columns are displayed on the main interface.
        """

        #----------------------- Create input columns window -------------------

        self.column_window = Toplevel(self.root)
        self.column_window.title("Select Columns")
        self.column_window.resizable(False, False)
        self.column_window.configure(bg="#dfe6e9")  

        title_frame = ctk.CTkFrame(
            self.column_window,
            fg_color="#2c3e50", 
            corner_radius=0
        )
        title_frame.pack(fill="x", pady=(10, 5), padx=0)  

        title_label = ctk.CTkLabel(
            title_frame,
            text="Select Input Columns",
            text_color="#ecf0f1",  
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=5)

        options_frame = ctk.CTkFrame(
            self.column_window,
            fg_color="#f1f2f6",  
            corner_radius=10
        )
        options_frame.pack(pady=(5, 5), padx=10, fill="both", expand=True)

        self.column_vars = {}
        if self.columns_selected != []:
            self.columns_selected = []
        for col in self.data_table["columns"]:
            var = IntVar()
            if col in self.columns_selected:
                var.set(1) 
            self.column_vars[col] = var

            checkbox = ctk.CTkCheckBox(
                options_frame,
                text=col,
                variable=var,
                text_color="#2c3e50", 
                fg_color="#3498db",  
                border_color="#7f8c8d",  
                hover_color="#2980b9"  
            )
            checkbox.pack(anchor="w", padx=15, pady=2) 
        button_frame = ctk.CTkFrame(
            self.column_window,
            fg_color="#dfe6e9"  
        )
        button_frame.pack(pady=(5, 10))  

        confirm_button = ctk.CTkButton(
            button_frame,
            text="Confirm Selection",
            command=self.confirm_selection,
            fg_color="#2ecc71",  
            hover_color="#27ae60",
            text_color="white",
            font=("Helvetica", 13),
            width=160  
        )
        confirm_button.pack(pady=3)  

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.column_window.destroy,
            fg_color="#e74c3c",  
            hover_color="#c0392b",
            text_color="white",
            font=("Helvetica", 13),
            width=160
        )
        cancel_button.pack(pady=3)

        self.column_window.update_idletasks()
        width = self.column_window.winfo_reqwidth() + 20
        height = self.column_window.winfo_reqheight() + 20
        self.column_window.geometry(f"{width}x{height}")

    def confirm_selection(self):
        """
        Confirm the selected input columns and update the label on the main interface.

        Displays a success message if columns are selected, or a warning if none are chosen.
        """

        self.columns_selected = [
            col for col, var in self.column_vars.items() if var.get() == 1
        ]

        if self.columns_selected:
            self.input_columns_label.configure(
                text=f"Input Columns: {', '.join(self.columns_selected)}"
            )
            self.column_window.destroy()
            
            messagebox.showinfo(
                "Columns Selected",
                f"Selected columns: {', '.join(self.columns_selected)}"
            )
            self.make_prediction_button.configure(state = "disabled")
        else:
            messagebox.showwarning(
                "No Selection",
                "No columns selected."
            )

    #-------------------------------------- OUTPUT COLUMN ---------------------------------

    def select_output_column(self):
        """
        Open a window to allow the user to select an output column from the data table.

        The selected column is displayed on the main interface.
        """

        #--------------------- Create output column window ---------------------

        self.output_column_window = Toplevel(self.root)
        self.output_column_window.title("Select Output Column")
        self.output_column_window.resizable(False, False)
        self.output_column_window.configure(bg="#dfe6e9")  

        title_frame = ctk.CTkFrame(
            self.output_column_window,
            fg_color="#2c3e50",  
            corner_radius=0
        )
        title_frame.pack(fill="x", pady=(10, 5), padx=0)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Select Output Column",
            text_color="#ecf0f1",  
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=5)

        options_frame = ctk.CTkFrame(
            self.output_column_window,
            fg_color="#f1f2f6",  
            corner_radius=10
        )
        options_frame.pack(pady=(5, 5), padx=10, fill="both", expand=True)

        self.output_column_var = ctk.StringVar(value="")  
        if self.output_column != None:
            self.output_column != None
        for col in self.data_table["columns"]:
            radiobutton = ctk.CTkRadioButton(
                    options_frame,
                    text=col,
                    variable=self.output_column_var,
                    value=col, 
                    text_color="#2c3e50",  
                    fg_color="#3498db",  
                    hover_color="#2980b9", 
                    border_color="#bdc3c7", 
                    border_width_checked=4  
                )
            radiobutton.pack(anchor="w", padx=15, pady=3)

            if col == self.output_column:
                self.output_column_var.set(col)

        button_frame = ctk.CTkFrame(
            self.output_column_window,
            fg_color="#dfe6e9"  
        )
        button_frame.pack(pady=(5, 10))

        confirm_button = ctk.CTkButton(
            button_frame,
            text="Confirm Selection",
            command=self.confirm_output_column,
            fg_color="#2ecc71",  
            hover_color="#27ae60",
            text_color="white",
            font=("Helvetica", 13),
            width=160 
        )
        confirm_button.pack(pady=3)

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.output_column_window.destroy,
            fg_color="#e74c3c",  
            hover_color="#c0392b",
            text_color="white",
            font=("Helvetica", 13),
            width=160
        )
        cancel_button.pack(pady=3)

        self.output_column_window.update_idletasks()
        width = self.output_column_window.winfo_reqwidth() + 20
        height = self.output_column_window.winfo_reqheight() + 20
        self.output_column_window.geometry(f"{width}x{height}")


    def confirm_output_column(self):
        """
        Confirm the selected output column and update the label on the main interface.

        Displays a success message if a column is selected, or a warning if none are chosen.
        """

        selected_output_column = self.output_column_var.get()
        if selected_output_column:
            messagebox.showinfo(
                "Output Column Selected",
                f"Selected Output Column: {selected_output_column}"
            )
            self.output_column = selected_output_column
            self.output_column_window.destroy()
            self.output_column_label.configure(
                text=f"Output Column: {self.output_column}"
            )
            self.make_prediction_button.configure(state = "disabled")
            self.create_model_button.configure(state="normal")
        else:
            messagebox.showwarning(
                "No Column Selected",
                "Please select an output column."
            )


