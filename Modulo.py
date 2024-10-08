import pandas as pd
import sqlite3

class data_import():
    def __init__(self):
        self._data = None

    def read_csv(self, file):
        try:
            self._data = pd.read_csv(file)
            return self._data
        except:
            print(f"File Not Found Error")
        
    def read_excel(self, file):
        try:
            self._data = pd.read_excel(file)
            return self._data
        except:
            print(f"File Not Found Error")
    
    def read_sqlite3(self, file):
        try:
            self._data = sqlite3.connect(file)
            return self._data
        except:
            print(f"File Not Found Error")
    
    def file_type(self, file):
        extension = file.split('.')
        if len(extension) < 2:
            return f"File format not found"
        pass
        


if __name__ == "__main__":        
    file_route = input("Introduce the file's route: ")
    file1 = file_route.replace("\\\\", "\\")
    
    x = data_import().read_csv(file1)
    y = data_import().read_excel(file1)
    print(x)
    print(y)
            
            
            

