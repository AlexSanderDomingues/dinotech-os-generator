import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
import os
from database import db
from ui.tela_principal import tela_principal

def tela_login(root):
    largura,altura = 600,700
    root.title("Dino Tech - Login")
    root.resizable(False,False)

    db.inicializar_banco() 

    for widget in root.winfo_children():
        widget.destroy()
    
    
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(dir_atual, "..", "assets", "login.png")
    caminho_imagem = os.path.abspath(caminho_imagem)

    if not os.path.exists(caminho_imagem):
        print("Imagem nao encontrada")
        return
    
    #carrega imagem
    imagem_fundo = Image.open(caminho_imagem)
    imagem_tk = CTkImage(light_image=imagem_fundo,dark_image=imagem_fundo, size=(600,700))
    fundo = ctk.CTkLabel(root, image = imagem_tk, text='')
    fundo.image = imagem_tk
    fundo.place(x=0,y=0, relwidth = 1 , relheight=1)

    #campos
    campo_user = ctk.CTkEntry(root,placeholder_text="Usuario", corner_radius=0, width=270,height=30)
    campo_user.place(relx=0.5, rely=0.55, x=-140, y=-45)

    campo_senha = ctk.CTkEntry(root, placeholder_text="Senha", show="*", corner_radius=0,width=270,height=30)
    campo_senha.place(relx = 0.5 , rely = 0.60, x=-140,y=-25)

    botao_login = ctk.CTkButton(root,text="Entrar",corner_radius=0,command=lambda:realizar_login())
    botao_login.place(relx = 0.5, rely = 0.67, x= -80 , y=-10)

    botao_cadastro = ctk.CTkButton(root,text="Cadastrar", corner_radius=0, command = lambda:realizar_cadastro(),width=200)
    botao_cadastro.place(relx = 0.5,rely=0.67,x=-110,y=40)
    
    # Label de mensagem criado por último
    label_mensagem = ctk.CTkLabel(root, text="", font=("Arial", 14),bg_color="#545555")
    label_mensagem.place(relx=0.5, rely=0.8, anchor='center')

    def mostrar_mensagem(texto, cor='white'):
        label_mensagem.configure(text=texto, text_color = cor)

    def realizar_login():
        usuario = campo_user.get()
        senha = campo_senha.get()

        if not usuario or not senha:
            mostrar_mensagem("Preencha todos os campos!","orange")
            return
        
        if db.verificar_login(usuario,senha):
            mostrar_mensagem("Login realizado com sucesso!","green")
            root.after(1000, lambda: tela_principal(root))
        else:
            mostrar_mensagem("Usuario ou senha incorretos.","red")
    
    def realizar_cadastro():
        usario = campo_user.get()
        senha = campo_senha.get()

        if db.cadastrar_usuario(usario,senha):
            mostrar_mensagem("Cadastros realizados com sucesso!","green")
        else:
            mostrar_mensagem("Usuario ja existe.","orange")