import customtkinter as ctk

class LogViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualizador de Logins")
        self.master.geometry("500x500")
        self.setup_gui()

    def setup_gui(self):
        self.frame = ctk.CTkFrame(self.master, width=480, height=480) 
        self.frame.pack(padx=10, pady=10, fill=ctk.BOTH, expand=True)  

        #criar um botão para carregar logs
        self.btn_load_logs = ctk.CTkButton(self.frame, text="Carregar Logs", command=self.load_logs)
        self.btn_load_logs.pack(pady=10)

        #criar um Textbox para exibir os logs, ocupando todo o espaço disponível
        self.txt_logs = ctk.CTkTextbox(self.frame)
        self.txt_logs.pack(padx=10, pady=10, fill=ctk.BOTH, expand=True) 

    def load_logs(self):
        self.txt_logs.delete("1.0", ctk.END)
        
        try:
            with open("gerence_loggins.log", "r") as log_file:
                logs = log_file.readlines()
                for log in logs:
                    self.txt_logs.insert(ctk.END, log)
        except FileNotFoundError:
            self.txt_logs.insert(ctk.END, "Arquivo de log não encontrado.")
        except Exception as e:
            self.txt_logs.insert(ctk.END, f"Erro ao carregar logs: {str(e)}")

if __name__ == '__main__':
    root = ctk.CTk()
    app = LogViewer(root)
    root.mainloop()