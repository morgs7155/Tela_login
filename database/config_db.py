import sqlite3



class Database():
    def __init__(self):
        self.Database_registrs()
        self.Database_helps()
        
    def Database_registrs(self):
        try:
            conn = sqlite3.connect('database/registers.db')
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER AUTOINCREMENTE PRIMARY KEY,
                    username TEXT,
                    password TEXT
                        );
                        """)
            
            conn.commit()
            conn.close()
            
        except:
            print(f'erro ao criar tabela{sqlite3.Error}')
            print(f'erro ao criar tabela{IndentationError}')
        
    def Database_helps(self):
        try:
            conn = sqlite3.connect('database/helps.db')
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Demands(
                    id INTEGER AUTOINCREMENTE PRIMARY KEY,
                    problem TEXT,
                    email,
                    date TEXT,
                    hour TEXT
                        );
                        """)
            
            conn.commit()
            conn.close()
        
        except:
            print(f'erro ao criar tabela{sqlite3.Error}')
            print(f'erro ao criar tabela{IndentationError}')
        
    
    
if __name__ == '__main__':
    Database()