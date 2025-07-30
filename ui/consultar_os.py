# ui/consultar_os.py
import customtkinter as ctk
from tkinter import messagebox
from database.db import listar_os
from utils.pdf import gerar_pdf_os
from datetime import datetime

def visualizar_os_detalhada(janela_pai, os_data):
    """Janela de visualização detalhada da OS"""
    detalhes_janela = ctk.CTkToplevel(janela_pai)
    detalhes_janela.title(f"Dino Tech - OS #{os_data[0]}")
    detalhes_janela.geometry("900x700")
    detalhes_janela.resizable(False, False)
    
    # Frame principal com scroll
    main_frame = ctk.CTkFrame(detalhes_janela)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    scroll_frame = ctk.CTkScrollableFrame(main_frame)
    scroll_frame.pack(fill="both", expand=True)
    
    # Título
    ctk.CTkLabel(
        scroll_frame,
        text=f"Ordem de Serviço #{os_data[0]}",
        font=("Arial", 20, "bold")
    ).pack(pady=(10, 20))
    
    # Dados formatados
    data_formatada = datetime.strptime(os_data[1], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
    
    # Função para criar campos
    def criar_campo(container, label, valor):
        frame = ctk.CTkFrame(container, fg_color="transparent")
        frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(
            frame,
            text=label,
            font=("Arial", 14, "bold"),
            width=200,
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            frame,
            text=valor if valor else "Não informado",
            font=("Arial", 14),
            anchor="w",
            wraplength=600,
            justify="left"
        ).pack(side="left", fill="x", expand=True)
    
    # Seção: Dados do Cliente
    ctk.CTkLabel(
        scroll_frame,
        text="DADOS DO CLIENTE",
        font=("Arial", 16, "bold"),
        anchor="w"
    ).pack(fill="x", pady=(10, 5), padx=10)
    
    criar_campo(scroll_frame, "Data:", data_formatada)
    criar_campo(scroll_frame, "Cliente:", os_data[2])
    criar_campo(scroll_frame, "Telefone:", os_data[3])
    
    # Seção: Dados Técnicos
    ctk.CTkLabel(
        scroll_frame,
        text="DADOS TÉCNICOS",
        font=("Arial", 16, "bold"),
        anchor="w"
    ).pack(fill="x", pady=(20, 5), padx=10)
    
    criar_campo(scroll_frame, "Aparelho/Modelo:", os_data[4])
    criar_campo(scroll_frame, "Problema Relatado:", os_data[5])
    criar_campo(scroll_frame, "Diagnóstico:", os_data[6])
    criar_campo(scroll_frame, "Solução Aplicada:", os_data[7])
    criar_campo(scroll_frame, "Técnico Responsável:", os_data[10])
    
    # Seção: Financeiro
    ctk.CTkLabel(
        scroll_frame,
        text="FINANCEIRO",
        font=("Arial", 16, "bold"),
        anchor="w"
    ).pack(fill="x", pady=(20, 5), padx=10)
    
    criar_campo(scroll_frame, "Valor:", f"R$ {float(os_data[8]):.2f}" if os_data[8] else "Não informado")
    criar_campo(scroll_frame, "Status:", os_data[9])
    criar_campo(scroll_frame, "Garantia:", os_data[11])
    
    # Botões
    btn_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    btn_frame.pack(pady=20)
    
    ctk.CTkButton(
        btn_frame,
        text="Gerar PDF",
        command=lambda: gerar_pdf_individual(os_data),
        width=150,
        height=40,
        fg_color="#4682B4"
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        btn_frame,
        text="Fechar",
        command=detalhes_janela.destroy,
        width=150,
        height=40,
        fg_color="#B22222"
    ).pack(side="left", padx=10)
    
    def gerar_pdf_individual(os):
        try:
            gerar_pdf_os(os)
            messagebox.showinfo("Sucesso", f"PDF da OS #{os[0]} gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar PDF: {str(e)}")
    
    detalhes_janela.transient(janela_pai)
    detalhes_janela.grab_set()
    detalhes_janela.focus_force()
    detalhes_janela.lift()


def consultar_os(root):
    janela = ctk.CTkToplevel(root)
    janela.title("Dino Tech - Consultar OS")
    janela.geometry("1200x800")
    janela.resizable(False, False)
    
    # Frame de filtros
    frame_filtros = ctk.CTkFrame(janela)
    frame_filtros.pack(pady=10, padx=10, fill="x")
    
    ctk.CTkLabel(frame_filtros, text="Filtrar:").pack(side="left", padx=5)
    
    entry_filtro = ctk.CTkEntry(frame_filtros, width=300)
    entry_filtro.pack(side="left", padx=5)
    
    btn_filtrar = ctk.CTkButton(
        frame_filtros, 
        text="Buscar",
        command=lambda: atualizar_lista()
    )
    btn_filtrar.pack(side="left", padx=5)
    
    # Lista de OS
    frame_lista = ctk.CTkFrame(janela)
    frame_lista.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Cabeçalho
    cabecalho = ctk.CTkFrame(frame_lista)
    cabecalho.pack(fill="x")
    
    colunas = ["ID", "Data", "Cliente", "Aparelho", "Status", "Valor", "Ações"]
    larguras = [50, 120, 200, 200, 100, 80, 150]
    
    for i, (coluna, largura) in enumerate(zip(colunas, larguras)):
        ctk.CTkLabel(
            cabecalho, 
            text=coluna,
            width=largura,
            anchor="w"
        ).grid(row=0, column=i, padx=2, sticky="w")
    
    # Scrollable frame para os resultados
    scroll_frame = ctk.CTkScrollableFrame(frame_lista)
    scroll_frame.pack(fill="both", expand=True)
    
    def atualizar_lista(filtro=None):
        # Limpa resultados anteriores
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        
        # Busca no banco de dados
        resultados = listar_os(filtro)
        
        if not resultados:
            ctk.CTkLabel(scroll_frame, text="Nenhuma OS encontrada").pack()
            return
        
        # Preenche os resultados
        for idx, os in enumerate(resultados):
            frame_os = ctk.CTkFrame(scroll_frame)
            frame_os.pack(fill="x", pady=2)
            
            # Formata a data
            data = datetime.strptime(os[1], '%Y-%m-%d %H:%M:%S')
            data_formatada = data.strftime('%d/%m/%Y %H:%M')
            
            # Exibe os dados
            ctk.CTkLabel(frame_os, text=os[0], width=50).grid(row=0, column=0, padx=2)
            ctk.CTkLabel(frame_os, text=data_formatada, width=120).grid(row=0, column=1, padx=2)
            ctk.CTkLabel(frame_os, text=os[2], width=200).grid(row=0, column=2, padx=2)
            ctk.CTkLabel(frame_os, text=os[4], width=200).grid(row=0, column=3, padx=2)
            ctk.CTkLabel(frame_os, text=os[9], width=100).grid(row=0, column=4, padx=2)
            ctk.CTkLabel(frame_os, text=f"R$ {os[8]:.2f}", width=80).grid(row=0, column=5, padx=2)
            
            # Botões de ação
            frame_botoes = ctk.CTkFrame(frame_os, fg_color="transparent")
            frame_botoes.grid(row=0, column=6, padx=2)
            
            btn_visualizar = ctk.CTkButton(
                frame_botoes,
                text="Visualizar",
                width=70,
                command=lambda o=os: visualizar_os_detalhada(janela,o)
            )
            btn_visualizar.pack(side="left", padx=2)
            
            btn_pdf = ctk.CTkButton(
                frame_botoes,
                text="PDF",
                width=50,
                command=lambda o=os: gerar_pdf(o)
            )
            btn_pdf.pack(side="left", padx=2)
    
    def gerar_pdf(os):
        try:
            gerar_pdf_os(os)
            messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar PDF: {str(e)}")
    
    # Atualiza a lista inicial
    atualizar_lista()

    janela.transient(root)
    janela.grab_set()
    janela.focus_force()
    janela.lift()
