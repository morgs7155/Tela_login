import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class Help():
    def __init__(self, master):
        self.master = master
        self.Setup()
        self.Date_hour()
        
    def Setup(self):
        self.Labels()
        self.Entrys()
        self.Buttons()

    def Labels(self):
        self.l_description = ctk.CTkLabel(self.master, text='descreva o problema:', font=('Times', 15, 'bold'), fg_color='white', 
                                          text_color='black')
        self.l_description.place(x=10, y=10)
        
        self.l_email = ctk.CTkLabel(self.master, text='email:', font=('Times', 15, 'bold'), fg_color='white', text_color='black')
        self.l_email.place(x=10, y=150)
    
    def Entrys(self):
        self.txt_description = ctk.CTkTextbox(self.master, width=380, height=100, font=('Arial', 12, 'bold'), fg_color='#ffffff', 
                                              border_width=2, border_color='black')
        self.txt_description.place(x=10, y=50)
        
        self.e_email = ctk.CTkEntry(self.master, width=380, font=('Arial', 12, 'bold'), border_color='black', border_width=2)
        self.e_email.place(x=10, y=180)
    
    def Buttons(self):
        self.btn_enviar = ctk.CTkButton(self.master, text='enviar',width=200, height=30, font=('Times', 12, 'bold'), fg_color='blue', 
                                        hover_color='lightblue', command=self.send_help)
        self.btn_enviar.place(x=100, y=230)
        
    def Date_hour(self):
        self.date_atual = datetime.now()
        
        self.format_date = self.date_atual.strftime("%d/%m/%Y")
        self.format_hour = self.date_atual.strftime("%H:%M:%S")
        
    def send_help(self):
        self.description = self.txt_description.get("1.0", "end-1c")
        self.email = self.e_email.get()
           
        try:
            conn = sqlite3.connect('database/helps.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Demands(problem, email, date, hour) VALUES(?,?,?,?)", (self.description, self.email, self.format_date, self.format_hour))
            conn.commit()
            conn.close()
            
            messagebox.showinfo('Solicitação', 'Solicitação enviada com sucesso')
            self.master.destroy()
            
        except sqlite3.Error as e:
            messagebox.showerror('ERROR', f'erro ao realizar reclamação {e}')
            
        except:
            messagebox.showerror("ERROR", f"{ValueError}")
        
    
if __name__ == '__main__':
    root = ctk.CTk()
    root.title('central de ajuda')
    app = Help(root)
    
    root.geometry('400x300')
    root.resizable(width=False, height=False)
    root.configure(fg_color = '#ffffff')
    
    root.mainloop()
    