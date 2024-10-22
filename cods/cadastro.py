import customtkinter as ctk
from tkinter import TOP, messagebox
from PIL import Image
import re
import subprocess as sp
import sqlite3
import logging
import bcrypt

cor_f = '#ffffff'

# Redirecionando os logs para um arquivo
logging.basicConfig(filename='gerence_loggins.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Cadastro():
    def __init__(self, master):
        self.master = master
        self.Setup()
        
    def Setup(self):
        self.Frames()
        self.Image()
        self.Icons()
        self.Labels()
        self.Entrys()
        self.Buttons()
    
    def Frames(self):
        self.f_center = ctk.CTkFrame(self.master, width=600, height=600, fg_color=cor_f)
        self.f_center.pack(side=TOP, expand=True)
        
    def Image(self):
        try:
            self.img_logo = Image.open('images/Pylife.png')
            self.img_logo_resize = self.img_logo.resize((300, 350), Image.Resampling.LANCZOS)
            self.img_logo_ofc = ctk.CTkImage(light_image=self.img_logo_resize, dark_image=self.img_logo_resize, size=(200, 120))
            
            self.l_icon_user = ctk.CTkLabel(self.f_center, text=None, image=self.img_logo_ofc, fg_color=cor_f)
            self.l_icon_user.place(x=190, y=20)
        
        except Exception as e:
            logging.error(f'Erro ao carregar imagem: {str(e)}')
            
        
    def Icons(self):
        # ícone de usuário 
        self.icon_user = Image.open('icons/usuarioalienigena.png')
        self.icon_user_resize = self.icon_user.resize((80, 80), Image.Resampling.LANCZOS)
        self.icon_user_ofc = ctk.CTkImage(self.icon_user_resize)
        
        # ícone de senha
        self.icon_tranca = Image.open('icons/trancar.png')
        self.icon_tranca_resize = self.icon_tranca.resize((80, 80), Image.Resampling.LANCZOS)
        self.icon_tranca_ofc = ctk.CTkImage(self.icon_tranca_resize)
        
        self.l_icon_user = ctk.CTkLabel(self.f_center, text=None, image=self.icon_user_ofc, fg_color=cor_f)
        self.l_icon_user.place(x=100, y=150)
            
        self.l_icon_pass = ctk.CTkLabel(self.f_center, text=None, image=self.icon_tranca_ofc, fg_color=cor_f)
        self.l_icon_pass.place(x=100, y=200)
        
        # Ícones de mostrar e ocultar senha
        self.icon_eye = Image.open('icons/olho.png').resize((25, 25), Image.Resampling.LANCZOS)
        self.icon_eye_crossed = Image.open('icons/olho_cruzado.png').resize((25, 25), Image.Resampling.LANCZOS)
        
        self.icon_eye_ofc = ctk.CTkImage(self.icon_eye)
        self.icon_eye_crossed_ofc = ctk.CTkImage(self.icon_eye_crossed)

            
    def Labels(self):
        self.info_pass = ctk.CTkLabel(self.f_center, 
                text=f'A senha deve conter:\nNo mínimo 8 caracteres\nNo máximo 20 caracteres\nUma letra minúscula\nUma letra maiúscula\nUm caractere especial',
                font=('Times', 15, 'bold'), fg_color=cor_f, text_color='black')
        self.info_pass.place(x=220, y=240)
    
    def Entrys(self):
        self.e_user = ctk.CTkEntry(self.f_center, width=300, placeholder_text='Crie um nome de usuário')
        self.e_user.place(x=150, y=150)
        
        self.e_pass = ctk.CTkEntry(self.f_center, width=300, placeholder_text='Crie uma senha', show='    ')
        self.e_pass.place(x=150, y=200)
        
        self.e_conf_pass = ctk.CTkEntry(self.f_center, width=300, placeholder_text='Confirme a senha', show='    ')
        self.e_conf_pass.place(x=150, y=350)
    
    def Buttons(self):
        self.btn_concluid = ctk.CTkButton(self.f_center, text='Cadastrar', font=('Times', 15, 'bold'), command=self.Insert_cadastro,  
                                          fg_color='black', text_color='#ffffff', width=100, height=30, hover_color='gray')
        self.btn_concluid.place(x=250, y=450)
        
        self.btn_login_ = ctk.CTkButton(self.f_center, command=self.Login, text='Já possui conta?', font=('Times', 15, 'bold'), fg_color='white', 
                                          text_color='#000000', width=100, height=30, hover_color='gray')
        self.btn_login_.place(x=240, y=500)
        
        self.btn_help = ctk.CTkButton(self.f_center, command=self.Help, text='Ajuda?', font=('Times', 15, 'bold'), fg_color='white', 
                                          text_color='#000000', width=100, height=30, hover_color='gray',)
        self.btn_help.place(x=250, y=550)
        
        self.btn_vizu = ctk.CTkButton(self.f_center, image=self.icon_eye_ofc, text=None, command=self.vizu_pass,
                                      fg_color='white', text_color='#000000', width=50, height=30, hover_color='gray')
        self.btn_vizu.place(x=450, y=200)
        
    def Help(self):
        sp.Popen(["python", "cods/ajuda.py"])
        
    def Login(self):
        sp.Popen(["python", "cods/login.py"])
        self.master.destroy()
        
    def vizu_pass(self):
        if self.e_pass.cget('show') == '    ':
            self.e_pass.configure(show='')
            self.btn_vizu.configure(image=self.icon_eye_crossed_ofc)
        else:
            self.e_pass.configure(show='    ')
            self.btn_vizu.configure(image=self.icon_eye_ofc)
        
    def validate_password(self, password):
        if len(password) < 8 or len(password) > 20:
            return 'A senha deve ter entre 8 e 20 caracteres'
        if not re.search(r'[a-z]', password):
            return 'A senha deve conter ao menos uma letra minúscula'
        if not re.search(r'[A-Z]', password):
            return 'A senha deve conter ao menos uma letra maiúscula'
        if not re.search(r'\W', password): 
            return 'A senha deve conter ao menos um caractere especial'
        return None 
    
    def hash_password(self, password):
        # Gerando um salt
        salt = bcrypt.gensalt()
        # Criptografando a senha
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password


    def Insert_cadastro(self):
        self.user = self.e_user.get()
        self.password = self.e_pass.get()
        self.conf_pass = self.e_conf_pass.get()

        # Verificar se os campos estão preenchidos
        if not self.user or not self.password or not self.conf_pass:
            messagebox.showerror('Atenção', 'Preencha todos os campos')
            logging.error('Tentativa de cadastro com campos em branco')
            return

        # Verificar a validação da senha
        password_error = self.validate_password(self.password)
        if password_error:
            messagebox.showerror('Atenção', password_error)
            logging.error('Tentativa de cadastro falhou: erro de validação de senha')
            return

        # Verificar se as senhas correspondem
        if self.password != self.conf_pass:
            messagebox.showerror('Atenção', 'Os campos de senha devem ser idênticos')
            logging.error('Tentativa de cadastro falhou: senhas não correspondem')
            return

        # Verificar se o nome de usuário já está cadastrado
        conn = sqlite3.connect('database/registers.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (self.user,))
        user_exists = cursor.fetchone()
        
        if user_exists:
            messagebox.showerror('Atenção', 'Nome de usuário já está em uso, escolha outro.')
            logging.warning(f'Tentativa de cadastro falhou: nome de usuário {self.user} já está cadastrado')
            conn.close()
            return

        # Inserir no banco de dados
        hashed_password = self.hash_password(self.password)
        cursor.execute('INSERT INTO users(username, password) VALUES(?, ?)', (self.user, hashed_password))

        conn.commit()
        conn.close()

        messagebox.showinfo('Cadastro', f'Usuário {self.user} cadastrado com sucesso')
        logging.info(f'Novo usuário cadastrado: {self.user}')
            
if __name__ == '__main__':
    root = ctk.CTk()
    root.title('pylife/Cadastro')
    
    app = Cadastro(root)
    
    # Tamanho de tela
    tela_width = root.winfo_screenwidth()
    tela_height = root.winfo_screenheight()
    root.geometry(f'{tela_width}x{tela_height}')
    
    root.mainloop()
