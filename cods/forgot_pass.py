import customtkinter as ctk
from tkinter import TOP, messagebox
from PIL import Image
import sqlite3
import bcrypt
import logging

cor_f = '#ffffff'

# Configurando o log
logging.basicConfig(filename='password_reset.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResetPass:
    def __init__(self, master):
        self.master = master
        self.Setup()
        
    def Setup(self):
        self.Frames()
        self.Icons()
        self.Entrys()
        self.Buttons()
    
    def Frames(self):
        self.f_center = ctk.CTkFrame(self.master, width=600, height=600, fg_color=cor_f)
        self.f_center.pack(side=TOP, expand=True)
    
    def Icons(self):
        # Ícones de usuário e senha
        self.icon_user = Image.open('icons/usuarioalienigena.png').resize((80, 80), Image.Resampling.LANCZOS)
        self.icon_tranca = Image.open('icons/trancar.png').resize((80, 80), Image.Resampling.LANCZOS)
        self.icon_eye = Image.open('icons/olho.png').resize((25, 25), Image.Resampling.LANCZOS)
        self.icon_eye_crossed = Image.open('icons/olho_cruzado.png').resize((25, 25), Image.Resampling.LANCZOS)
        
        self.icon_user_ofc = ctk.CTkImage(self.icon_user)
        self.icon_tranca_ofc = ctk.CTkImage(self.icon_tranca)
        self.icon_eye_ofc = ctk.CTkImage(self.icon_eye)
        self.icon_eye_crossed_ofc = ctk.CTkImage(self.icon_eye_crossed)
        
        # Exibindo ícones
        self.l_icon_user = ctk.CTkLabel(self.f_center, text=None, image=self.icon_user_ofc, fg_color=cor_f)
        self.l_icon_user.place(x=100, y=150)
        
        self.l_icon_pass = ctk.CTkLabel(self.f_center, text=None, image=self.icon_tranca_ofc, fg_color=cor_f)
        self.l_icon_pass.place(x=100, y=200)
        
    def Entrys(self):
        self.e_user = ctk.CTkEntry(self.f_center, width=300, placeholder_text='Digite seu nome de usuário')
        self.e_user.place(x=150, y=150)
        
        self.e_new_pass = ctk.CTkEntry(self.f_center, width=300, placeholder_text='Digite sua nova senha', show='    ')
        self.e_new_pass.place(x=150, y=200)
        
    def Buttons(self):
        self.btn_reset = ctk.CTkButton(self.f_center, text='Redefinir Senha', font=('Times', 15, 'bold'), command=self.ResetPassword,  
                                       fg_color='black', text_color='#ffffff', width=150, height=30, hover_color='gray')
        self.btn_reset.place(x=230, y=250)
        
        self.btn_show = ctk.CTkButton(self.f_center, image=self.icon_eye_ofc, text=None, command=self.TogglePassword,
                                      fg_color='white', width=50, height=30, hover_color='gray')
        self.btn_show.place(x=450, y=200)
    
    def TogglePassword(self):
        if self.e_new_pass.cget('show') == '    ':
            self.e_new_pass.configure(show='')
            self.btn_show.configure(image=self.icon_eye_crossed_ofc)
        else:
            self.e_new_pass.configure(show='    ')
            self.btn_show.configure(image=self.icon_eye_ofc)
    
    def ResetPassword(self):
        self.user = self.e_user.get()
        self.new_password = self.e_new_pass.get()
        
        # Validação de entrada
        if not self.user or not self.new_password:
            messagebox.showerror('Erro', 'Preencha todos os campos')
            logging.error('Campos de redefinição de senha vazios')
            return
        
        # Criptografar a nova senha
        hashed_password = bcrypt.hashpw(self.new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Conectar ao banco de dados e verificar se o usuário existe
        try:
            conn = sqlite3.connect('database/registers.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = ?", (self.user,))
            result = cursor.fetchone()
            
            if result:
                # Atualizar a senha no banco de dados
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, self.user))
                conn.commit()
                messagebox.showinfo('Sucesso', 'Senha redefinida com sucesso!')
                logging.info(f'Senha redefinida para o usuário: {self.user}')
            else:
                messagebox.showerror('Erro', 'Usuário não encontrado')
                logging.error(f'Tentativa de redefinição de senha para usuário inexistente: {self.user}')
                
        except sqlite3.Error as e:
            messagebox.showerror('Erro', f'Erro no banco de dados: {str(e)}')
            logging.error(f'Erro no banco de dados: {str(e)}')
        finally:
            conn.close()
            
        self.master.destroy()

if __name__ == '__main__':
    root = ctk.CTk()
    root.title('Redefinir Senha')
    
    app = ResetPass(root)
    
    # Configurações de tamanho da tela
    tela_width = root.winfo_screenwidth()
    tela_height = root.winfo_screenheight()
    root.geometry(f'{tela_width}x{tela_height}')
    
    root.mainloop()
