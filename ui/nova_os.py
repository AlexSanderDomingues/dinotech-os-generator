# ui/nova_os.py
import customtkinter as ctk
import sqlite3
import re
from datetime import datetime
from tkinter import messagebox
import os
import sys

def nova_os(root):
    # Configuração da janela
    janela = ctk.CTkToplevel(root)
    janela.title("Dino Tech - Nova Ordem de Serviço")
    janela.geometry("900x650")
    janela.resizable(False, False)
    
    
    # Centralizar na tela
    largura, altura = 900, 650
    screen_width = janela.winfo_screenwidth()
    screen_height = janela.winfo_screenheight()
    x = (screen_width - largura) // 2
    y = (screen_height - altura) // 2
    janela.geometry(f"+{x}+{y}")
    
    # Configurar fonte (como no seu código principal)
    fonte_grande = ("Arial", 16, "bold")
    fonte_normal = ("Arial", 14)
    
    # Frame principal
    frame_principal = ctk.CTkFrame(janela)
    frame_principal.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Título
    ctk.CTkLabel(
        frame_principal,
        text="Nova Ordem de Serviço",
        font=("Arial", 40, "bold")
    ).pack(pady=20)
    
    # Campos do formulário
    campos = [
        ("Nome do Cliente", "entry_cliente"),
        ("Telefone/WhatsApp", "entry_telefone"),
        ("Aparelho/Modelo", "entry_aparelho"),
        ("Problema Relatado", "entry_problema"),
        ("Diagnóstico Técnico", "entry_diagnostico"),
        ("Solução Aplicada", "entry_solucao"),
        ("Valor do Serviço", "entry_valor")
    ]
    
    for label, nome in campos:
        frame = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(frame, text=label, font=fonte_normal).pack(side="left")
        
        entry = ctk.CTkEntry(frame, corner_radius=0,font=fonte_normal,width=300)
        entry.place(relx = 0.5 , rely = 0.67 , x=-220, y=-20)
        setattr(janela, nome, entry)  # Guarda referência
        
        # Configuração especial para campo de valor
        if nome == "entry_valor":
            entry.configure(placeholder_text="R$ 0,00")
    
    # Frame para status e botões
    frame_rodape = ctk.CTkFrame(frame_principal)
    frame_rodape.pack(fill="x", pady=20, padx=10)
    
    # Status
    ctk.CTkLabel(frame_rodape, text="Status:", font=fonte_normal).pack(side="left", padx=5)
    
    status_var = ctk.StringVar(value="Aberta")
    status_opcoes = ["Aberta", "Em andamento", "Finalizada"]
    
    for status in status_opcoes:
        rb = ctk.CTkRadioButton(
            frame_rodape,
            text=status,
            variable=status_var,
            value=status,
            font=fonte_normal
        )
        rb.pack(side="left", padx=5)
    
    # Botões
    frame_botoes = ctk.CTkFrame(frame_principal,corner_radius=0, fg_color="transparent")
    frame_botoes.pack(fill="x", pady=10)
    
    ctk.CTkButton(
        frame_botoes,
        text="Salvar OS",
        font=fonte_grande,
        height=40,
        command=lambda: validar_e_salvar(janela, status_var.get())
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        frame_botoes,
        text="Cancelar",
        font=fonte_grande,
        height=40,
        fg_color="gray",
        command=janela.destroy
    ).pack(side="right", padx=10)
    
    janela.transient(root)       # Corrige o nome
    janela.grab_set()            # Impede interação com a janela principal enquanto a nova estiver aberta
    janela.focus_force()         # Dá o foco
    janela.lift()                # Garante que ela fique no topo



def validar_e_salvar(janela, status):
    # Coletar dados dos campos
    dados = {
        'cliente': janela.entry_cliente.get().strip(),
        'telefone': janela.entry_telefone.get().strip(),
        'aparelho': janela.entry_aparelho.get().strip(),
        'problema': janela.entry_problema.get().strip(),
        'diagnostico': janela.entry_diagnostico.get().strip(),
        'solucao': janela.entry_solucao.get().strip(),
        'valor': janela.entry_valor.get().strip()
    }

    # Validação dos campos
    erros = []
    
    if not dados['cliente']:
        erros.append("Nome do cliente é obrigatório")
    
    if not dados['telefone']:
        erros.append("Telefone é obrigatório")
    elif not re.match(r'^(\+?55)?[ -]?(\(?\d{2}\)?[ -]?)?\d{4,5}[ -]?\d{4}$', dados['telefone']):
        erros.append("Telefone inválido")
    
    if not dados['aparelho']:
        erros.append("Aparelho/Modelo é obrigatório")
    
    if not dados['problema']:
        erros.append("Problema relatado é obrigatório")
    
    try:
        valor = float(dados['valor'].replace('R$', '').replace(',', '.').strip())
    except:
        erros.append("Valor inválido (use números com vírgula ou ponto)")
    
    if erros:
        messagebox.showerror("Erros no Formulário", "\n".join(erros))
        return
    
    # Conexão com o banco de dados
    try:
        
        def get_caminho_banco():
            if getattr(sys, 'frozen', False):
                # Se estiver rodando como .exe (PyInstaller)
                base_path = sys._MEIPASS
            else:
                # Rodando via script normal
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            return os.path.join(base_path, 'database', 'usuario.db')
        

        conn = sqlite3.connect(get_caminho_banco())
        cursor = conn.cursor()
        
        # Inserir no banco de dados
        cursor.execute('''
        INSERT INTO ordens_servico (
            data_criacao,
            nome_cliente,
            telefone,
            aparelho_modelo,
            problema_relatado,
            diagnostico,
            solucao,
            valor,
            status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            dados['cliente'],
            dados['telefone'],
            dados['aparelho'],
            dados['problema'],
            dados['diagnostico'],
            dados['solucao'],
            valor,
            status
        ))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", "Ordem de Serviço cadastrada com sucesso!")
        janela.destroy()
        
    except sqlite3.Error as e:
        messagebox.showerror("Erro no Banco de Dados", f"Erro ao salvar OS:\n{str(e)}")

 