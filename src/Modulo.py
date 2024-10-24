import pandas as pd
import sqlite3


class DataImport():
    
    def __init__(self, file):

        self._file = file
        self._data = None
    
    def read_csv(self):
        try:
            self._data = pd.read_csv(self._file)
            if self._data.empty:
                print("\nCSV file is empty\n")
        except pd.errors.ParserError:
            print("\nCorrupt file\n")
        except FileNotFoundError:
            print("\nFile not found")
        except:
            print("\nNot valid route")


    def read_excel(self):
        try:
            self._data = pd.read_excel(self._file)
            if self._data.empty:
                print("\nExcel file is empty\n")
        except ValueError:
            print("\nData error\n")
        except FileNotFoundError:
            print("\nFile not found")
        except:
            print("\nNot valid route")

    def read_sql(self):
        try:
            db_connection = sqlite3.connect(self._file)
            cursor = db_connection.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type= 'table';")
            tables = cursor.fetchall()
            
            if len(tables) == 0:
                raise Exception("\nNo tables found in the database\n")
            
            table_name = tables[0][0]
            print(f"\nTable '{table_name}' found.\n")
            
            self._data = pd.read_sql(f"SELECT * FROM {table_name}", db_connection)
        except sqlite3.DatabaseError:
            print("\nCorrupt file\n")
        except FileNotFoundError:
            print("\nFile not found")
        except:
            print("\nNot valid route")
        finally:
            if db_connection:
                db_connection.close()

    def file_type(self):
        partes = self._file.split('.')
        if len(partes) < 2:
            print("\nFile format not found\n")
        else:
            extension = partes[1].lower()
            if extension == "csv":
                self.read_csv()
            elif extension == "xlsx" or extension == "xls":
                self.read_excel()
            elif extension == "db" or extension == "sqlite":
                self.read_sql()
            else:
                print("\nFormat not valid\n")


    def read_file(self):
        self.file_type()
        if self._data is not None:
            print(self._data)
            return self._data

if __name__ == "__main__":
    file = input("Introduce the file's route: ").replace("\\\\", "\\")
    DataImport(file).read_file()

            
            

