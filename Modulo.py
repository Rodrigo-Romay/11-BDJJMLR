import pandas as pd
import sqlite3

class data_import():
    def __init__(self):
        self._data = None
        self._file = None

    def read_csv(self):
        self._data = pd.read_csv(self._file)
        return self._data
        
    def read_excel(self):
        self._data = pd.read_excel(self._file)
        return self._data
    def read_sql(self):
        self._data = sqlite3.connect(self._file)
        return self._data

    def file_type(self):
        try:
            partes = self._file.split('.')
            if len(partes) < 2:
                print("File format not found")
            else:
                extension = partes[1].lower()
                if extension == "csv":
                    self.read_csv()
                elif extension == "xlsx":
                    self.read_excel()
                elif extension == "db":
                    self.read_sql()
                else:
                    print("\nFormat not valid")
        except FileNotFoundError:
            print("\nError: File not found")
    
    def ask_file(self):
        self._file = input("Introduce the file's route: ").replace("\\\\", "\\")

    def read_file(self):
        self.ask_file()
        self.file_type()
        return self._data


if __name__ == "__main__":
    x = data_import().read_file()
            
            

