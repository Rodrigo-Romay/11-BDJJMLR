import pandas as pd
import sqlite3
from tkinter import messagebox


#=================================== DATAIMPORT ==================================

class DataImport():
    """Handles the import of various file types (CSV, Excel, SQLite) and converts them into a pandas DataFrame."""

    def __init__(self, file):
        """Initializes the DataImport class with the specified file path.

        Args:
            file (str): Path to the file to be imported.
        """

        self._file = file
        self._data = None

    #--------------------------- READ BY EXTENSION TYPE -------------------------

    def read_csv(self):
        """Reads a CSV file and loads its content into a pandas DataFrame.

        Raises:
            ParserError: If the file is corrupt.
            FileNotFoundError: If the file is not found at the specified path.
        """

        try:
            self._data = pd.read_csv(self._file)
        except pd.errors.ParserError:
            messagebox.showerror("Error", "The CSV file is corrupt.")
        except FileNotFoundError:
            messagebox.showerror("Error", "The file was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def read_excel(self):
        """Reads an Excel file and loads its content into a pandas DataFrame.

        Raises:
            ValueError: If there is an error in the data.
            FileNotFoundError: If the file is not found at the specified path.
        """

        try:
            self._data = pd.read_excel(self._file)
        except ValueError:
            messagebox.showerror("Error", "The Excel file is corrupt.")
        except FileNotFoundError:
            messagebox.showerror("Error", "The file was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def read_sql(self):
        """Reads data from an SQLite database and loads its first table into a pandas DataFrame.

        Raises:
            Exception: If no tables are found in the database.
            DatabaseError: If the database file is corrupt.
            FileNotFoundError: If the database file is not found at the specified path.
        """

        try:
            db_connection = sqlite3.connect(self._file)
            cursor = db_connection.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type= 'table';")
            tables = cursor.fetchall()

            if len(tables) == 0:
                raise Exception("\nNo tables found in the database\n")

            table_name = tables[0][0]
            messagebox.showinfo("Info", f"Table '{table_name}' found in the database.")

            self._data = pd.read_sql(f"SELECT * FROM {table_name}", db_connection)
        except sqlite3.DatabaseError:
            messagebox.showerror("Error", "The database file is corrupt.")
        except FileNotFoundError:
            messagebox.showerror("Error", "The file was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            if db_connection:
                db_connection.close()

    #------------------------- DISTINGUISH EXTENSION TYPE -------------------------

    def file_type(self):
        """Determines the file type based on its extension and calls the appropriate reading method.

        Supported formats:
            - CSV
            - Excel (XLSX, XLS)
            - SQLite (DB)
        """

        partes = self._file.split('.')
        if len(partes) < 2:
            messagebox.showwarning("Warning", "The file format could not be determined.")
        else:
            extension = partes[1].lower()
            if extension == "csv":
                self.read_csv()
            elif extension == "xlsx" or extension == "xls":
                self.read_excel()
            elif extension == "db" or extension == "sqlite":
                self.read_sql()
            else:
                messagebox.showwarning("Warning", "Unsupported file format.")

    #--------------------------------- READ FILE -------------------------------

    def read_file(self):
        """Reads the file and returns its content as a pandas DataFrame.

        Returns:
            pandas.DataFrame: Data read from the file.
        """

        self.file_type()
        if self._data is not None:
            print(self._data)
            return self._data


if __name__ == "__main__":
    file = input("Introduce the file's route: ").replace("\\\\", "\\")
    DataImport(file).read_file()
