import customtkinter as ctk
from PIL import Image
import os
from customtkinter import CTkImage
from utils.utils import centralizar_janela
from ui.nova_os import nova_os
from ui.consultar_os import consultar_os

def tela_principal(root):
    largura, altura = 1200, 800
    root.title("Dino Tech - Sistema OS")
    root.geometry("1200x800")
    centralizar_janela(root, largura, altura)
    root.resizable(False, False)

    for widget in root.winfo_children():
        widget.destroy()
    
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(dir_atual, "..", "assets", "Tela_inicial.png")
    caminho_imagem = os.path.abspath(caminho_imagem)
    
    if not os.path.exists(caminho_imagem):
        print("Imagem nao encontrada")
        return
    
    # Carrega imagem
    imagem_fundo = Image.open(caminho_imagem)
    imagem_tk = CTkImage(light_image=imagem_fundo, dark_image=imagem_fundo, size=(1200, 800))
    fundo = ctk.CTkLabel(root, image=imagem_tk, text='')
    fundo.image = imagem_tk
    fundo.place(x=0, y=0, relwidth=1, relheight=1)

    # Configuração de fonte para os botões
      # Fonte aumentada e em negrito

    # Botão Nova OS com fonte maior
    btn_nova_os = ctk.CTkButton(
        root,
        text="Nova OS",
        corner_radius=0,
        height=100,
        # Adicionado parâmetro de fonte
        command=lambda: nova_os(root)
    )
    btn_nova_os.place(relx=0.5, rely=0.67, x=-200, y=-140)

    # Botão Consultar com fonte maior
    btn_consultar = ctk.CTkButton(
        root,
        text="Consultar OS",
        corner_radius=0,
        height=100,
      # Adicionado parâmetro de fonte
        command=lambda: consultar_os(root)
    )
    btn_consultar.place(relx=0.5, rely=0.67, x=10, y=-140)