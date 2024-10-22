import customtkinter as ctk
from tkinter import TOP, messagebox
from PIL import Image
import subprocess as sp
import sqlite3
import logging
import bcrypt

cor_f = '#ffffff'

# Redirecionando os logs para um arquivo
logging.basicConfig(filename='gerence_loggins.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Login():
    def __init__(self, master):
        self.master = master
        self.setup()
        
    def setup(self):
        self.frames()
        self.load_images()
        self.labels_and_icons()
        self.entry_widgets()
        self.buttons()
    
    def frames(self):
        self.f_center = ctk.CTkFrame(self.master, width=600, height=600, fg_color=cor_f)
        self.f_center.pack(side=TOP, expand=True)
        
    def load_images(self):
        try:
            # Carregar logo
            self.img_logo = Image.open('images/Pylife.png').resize((300, 350), Image.Resampling.LANCZOS)
            self.img_logo_ofc = ctk.CTkImage(light_image=self.img_logo, dark_image=self.img_logo, size=(200, 120))
            
            # Ícones de usuário e senha
            self.icon_user = Image.open('icons/usuarioalienigena.png').resize((80, 80), Image.Resampling.LANCZOS)
            self.icon_tranca = Image.open('icons/trancar.png').resize((80, 80), Image.Resampling.LANCZOS)

            # Ícones de mostrar e ocultar senha
            self.icon_eye = Image.open('icons/olho.png').resize((25, 25), Image.Resampling.LANCZOS)
            self.icon_eye_crossed = Image.open('icons/olho_cruzado.png').resize((25, 25), Image.Resampling.LANCZOS)
            
            self.icon_eye_ofc = ctk.CTkImage(self.icon_eye)
            self.icon_eye_crossed_ofc = ctk.CTkImage(self.icon_eye_crossed)

        except Exception as e:
            logging.error(f'Erro ao carregar imagem: {e}')
    
    def labels_and_icons(self):
        # Logo
        ctk.CTkLabel(self.f_center, text=None, image=self.img_logo_ofc, fg_color=cor_f).place(x=190, y=20)
        
        # Ícone de usuário
        self.icon_user_ofc = ctk.CTkImage(self.icon_user)
        ctk.CTkLabel(self.f_center, text=None, image=self.icon_user_ofc, fg_color=cor_f).place(x=100, y=150)
        
        # Ícone de senha
        self.icon_tranca_ofc = ctk.CTkImage(self.icon_tranca)
        ctk.CTkLabel(self.f_center, text=None, image=self.icon_tranca_ofc, fg_color=cor_f).place(x=100, y=200)
            
    def entry_widgets(self):
        self.e_user = ctk.CTkEntry(self.f_center, width=300, placeholder_text='Digite seu nome de usuário')
        self.e_user.place(x=150, y=150)
        
        self.e_pass = ctk.CTkEntry(self.f_center, width=300, placeholder_text='Digite sua senha', show='    ')
        self.e_pass.place(x=150, y=200)
    
    def buttons(self):
        button_config = {'font': ('Times', 15, 'bold'), 'width': 100, 'height': 30, 'hover_color': 'gray'}

        ctk.CTkButton(self.f_center, text='Entrar', command=self.conf_cadastro, 
                      fg_color='black', text_color='#ffffff', **button_config).place(x=250, y=250)
        
        ctk.CTkButton(self.f_center, text='Não possui conta?', command=self.cadastro,
                      fg_color='white', text_color='#000000', **button_config).place(x=235, y=300)
        
        ctk.CTkButton(self.f_center, text='Ajuda?', command=self.help,
                      fg_color='white', text_color='#000000', **button_config).place(x=250, y=350)
        
        ctk.CTkButton(self.f_center, text='esqueceu sua senha?', command=self.Amnesia,
                      fg_color='white', text_color='#000000', **button_config).place(x=228, y=400)
        
        # Botão de mostrar/ocultar senha com ícones
        self.btn_vizu = ctk.CTkButton(self.f_center, image=self.icon_eye_ofc, text=None, command=self.vizu_pass,
                                      fg_color='white', text_color='#000000', width=50, height=30, hover_color='gray')
        self.btn_vizu.place(x=450, y=200)
        
    def help(self):
        sp.Popen(["python", "cods/ajuda.py"])
        
    def cadastro(self):
        sp.Popen(["python", "cods/cadastro.py"])
        self.master.destroy()
        
    def vizu_pass(self):
        if self.e_pass.cget('show') == '    ':
            self.e_pass.configure(show='')
            self.btn_vizu.configure(image=self.icon_eye_crossed_ofc)
        else:
            self.e_pass.configure(show='    ')
            self.btn_vizu.configure(image=self.icon_eye_ofc)
    
    def Amnesia(self):
        sp.Popen(["python", "cods/forgot_pass.py"])
        root.iconify()

    def conf_cadastro(self):
        user = self.e_user.get()
        password = self.e_pass.get()

        if not user or not password:
            messagebox.showerror('Atenção', 'Preencha todos os campos')
            logging.error('Tentativa de login com campos em branco')
            return

        with sqlite3.connect('database/registers.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (user,))
            result = cursor.fetchone()

            if result:
                stored_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    messagebox.showinfo('Sucesso', 'Login realizado com sucesso!')
                    logging.info(f'Usuário {user} fez login com sucesso')
                else:
                    messagebox.showerror('Erro', 'Senha incorreta')
                    logging.error(f'Tentativa de login com senha incorreta para o usuário {user}')
            else:
                messagebox.showerror('Erro', 'Usuário não encontrado')
                logging.error(f'Tentativa de login com usuário inexistente: {user}')


if __name__ == '__main__':
    root = ctk.CTk()
    root.title('Login')
    root.title('Pylife/login')
    
    app = Login(root)
    
    # Configurações de tamanho da tela
    tela_width = root.winfo_screenwidth()
    tela_height = root.winfo_screenheight()
    root.geometry(f'{tela_width}x{tela_height}')
    
    root.mainloop()
