import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Constante para o nome do arquivo do banco de dados ---
DATA_FILE = "database.json"


def load_users():
    """Carrega os usuários do arquivo JSON. Retorna uma lista vazia se o arquivo não existir."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            # Se o arquivo estiver vazio, json.load() dará erro.
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_users(users_list):
    """Salva a lista de usuários no arquivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_list, f, indent=4, ensure_ascii=False)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Variáveis de estado (para o easter egg) ---
        self.cont = 0
        self.Tcont = 0

        # --- Configuração da Janela Principal ---
        self.title("MarciotiSistem")
        self.geometry("400x350")

        # --- Estilo (simulando o tema 'Dark') ---
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        dark_bg = '#2d2d2d'
        light_fg = '#ffffff'
        entry_bg = '#4f4f4f'
        button_active_bg = '#6a6a6a'

        self.style.configure('.', background=dark_bg, foreground=light_fg)
        self.style.configure('TFrame', background=dark_bg)
        self.style.configure('TLabel', background=dark_bg, foreground=light_fg, font=('Arial', 10))
        self.style.configure('TButton', background=dark_bg, foreground=light_fg, font=('Arial', 10))
        self.style.map('TButton', background=[('active', button_active_bg)])
        self.style.configure('TEntry', fieldbackground=entry_bg, foreground=light_fg, insertbackground=light_fg)

        self.configure(bg=dark_bg)

        # --- Container para os frames (telas) ---
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SistemaFrame, CadastroFrame, LoginFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SistemaFrame)

    def show_frame(self, cont):
        """Mostra um frame para a classe de frame passada como argumento."""
        frame = self.frames[cont]
        frame.tkraise()

    def handle_nt_click(self):
        """Gerencia a lógica do botão 'NT'."""
        # A lógica do easter egg permanece a mesma
        self.cont += 1
        if self.cont == 100:
            messagebox.showinfo("Aviso", "se gosta de clicar, clica então")
            # ... (código do easter egg omitido para brevidade)


class SistemaFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="20")

        label = ttk.Label(self, text="BEM VINDO, ESCOLHA SUA OPÇÃO", font=("Arial", 12, "bold"))
        label.pack(pady=20)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        btn_cadastrar = ttk.Button(btn_frame, text="Cadastrar",
                                   command=lambda: controller.show_frame(CadastroFrame))
        btn_cadastrar.pack(side="left", padx=10)

        btn_entrar = ttk.Button(btn_frame, text="Entrar",
                                command=lambda: controller.show_frame(LoginFrame))
        btn_entrar.pack(side="left", padx=10)

        btn_nt = ttk.Button(btn_frame, text="NT", command=controller.handle_nt_click)
        btn_nt.pack(side="left", padx=10)


class CadastroFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="20")
        self.controller = controller
        self.columnconfigure(1, weight=1)

        # --- Widgets do formulário de cadastro ---
        ttk.Label(self, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        self.nome_entry = ttk.Entry(self)
        self.nome_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Idade:").grid(row=2, column=0, sticky="w", pady=5)
        self.idade_entry = ttk.Entry(self)
        self.idade_entry.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Senha:").grid(row=3, column=0, sticky="w", pady=5)
        self.senha_entry = ttk.Entry(self, show="*")
        self.senha_entry.grid(row=3, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Confirme a senha:").grid(row=4, column=0, sticky="w", pady=5)
        self.confir_entry = ttk.Entry(self, show="*")
        self.confir_entry.grid(row=4, column=1, sticky="ew", pady=5)

        # --- Botões ---
        btn_voltar = ttk.Button(self, text="Voltar",
                                command=lambda: controller.show_frame(SistemaFrame))
        btn_voltar.grid(row=5, column=0, pady=20, sticky="w")

        btn_cadastrar_dados = ttk.Button(self, text="Cadastrar Dados", command=self.handle_cadastro)
        btn_cadastrar_dados.grid(row=5, column=1, pady=20, sticky="e")

    def handle_cadastro(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        idade = self.idade_entry.get()
        senha = self.senha_entry.get()
        confir_senha = self.confir_entry.get()

        if not all([nome, email, idade, senha, confir_senha]):
            messagebox.showwarning("Erro de Cadastro", "Por favor, preencha todos os campos.")
            return

        if senha != confir_senha:
            messagebox.showerror("Erro de Cadastro", "As senhas não coincidem!")
            return

        users = load_users()

        # Verifica se o e-mail já está em uso
        for user in users:
            if user['email'] == email:
                messagebox.showerror("Erro de Cadastro", "Este e-mail já está cadastrado.")
                return

        # Adiciona o novo usuário
        new_user = {
            "nome": nome,
            "email": email,
            "idade": idade,
            "senha": senha  # Em um app real, a senha deve ser criptografada!
        }
        users.append(new_user)
        save_users(users)

        messagebox.showinfo("Sucesso", f"Usuário {nome} cadastrado com sucesso!")
        self.clear_fields()
        # Volta para a tela de login após o cadastro
        self.controller.show_frame(LoginFrame)

    def clear_fields(self):
        """Limpa todos os campos de entrada."""
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.idade_entry.delete(0, tk.END)
        self.senha_entry.delete(0, tk.END)
        self.confir_entry.delete(0, tk.END)


class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="20")
        self.columnconfigure(1, weight=1)

        # --- Widgets do formulário de login ---
        ttk.Label(self, text="Email:").grid(row=0, column=0, sticky="w", pady=10)
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=0, column=1, sticky="ew", pady=10)

        ttk.Label(self, text="Senha:").grid(row=1, column=0, sticky="w", pady=10)
        self.senha_entry = ttk.Entry(self, show="*")
        self.senha_entry.grid(row=1, column=1, sticky="ew", pady=10)

        # --- Botões ---
        btn_voltar = ttk.Button(self, text="Voltar",
                                command=lambda: controller.show_frame(SistemaFrame))
        btn_voltar.grid(row=2, column=0, pady=20, sticky="w")

        btn_entrar = ttk.Button(self, text="Entrar", command=self.handle_login)
        btn_entrar.grid(row=2, column=1, pady=20, sticky="e")

    def handle_login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if not all([email, senha]):
            messagebox.showwarning("Erro de Login", "Preencha E-mail e Senha.")
            return

        users = load_users()

        for user in users:
            if user['email'] == email and user['senha'] == senha:
                messagebox.showinfo("Login Bem-sucedido", f"Bem-vindo, {user['nome']}!")
                self.clear_fields()
                # Aqui você poderia navegar para uma nova tela principal do app
                return

        messagebox.showerror("Erro de Login", "E-mail ou senha inválidos.")

    def clear_fields(self):
        """Limpa os campos de entrada."""
        self.email_entry.delete(0, tk.END)
        self.senha_entry.delete(0, tk.END)


if __name__ == "__main__":
    app = App()
    app.mainloop()
