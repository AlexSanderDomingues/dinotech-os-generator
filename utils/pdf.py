# utils/pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

def gerar_pdf_os(os_data):
    # Dados da OS
    id_os, data, cliente, telefone, aparelho, problema, diagnostico, solucao, valor, status, *_ = os_data
    
    # Formata a data
    data_formatada = datetime.strptime(data, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
    
    # Nome do arquivo
    filename = f"OS_{id_os}_{cliente.replace(' ', '_')}.pdf"
    
    # Cria o PDF
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Estilos
    styles = getSampleStyleSheet()
    style_title = styles['Title']
    style_normal = styles['BodyText']
    
    # Cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Dino Tech - Ordem de Serviço")
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 130, f"OS Nº: {id_os} - Data: {data_formatada}")
    
    # Informações do cliente
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 180, "Cliente:")
    c.setFont("Helvetica", 12)
    c.drawString(180, height - 180, cliente)
    
    c.drawString(100, height - 200, "Telefone:")
    c.drawString(180, height - 200, telefone)
    
    # Dados do serviço
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 240, "Aparelho/Modelo:")
    c.setFont("Helvetica", 12)
    c.drawString(220, height - 240, aparelho)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 260, "Problema Relatado:")
    c.setFont("Helvetica", 12)
    problema_paragraph = Paragraph(problema, style_normal)
    problema_paragraph.wrapOn(c, 400, 100)
    problema_paragraph.drawOn(c, 220, height - 280)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 320, "Diagnóstico Técnico:")
    c.setFont("Helvetica", 12)
    diagnostico_paragraph = Paragraph(diagnostico if diagnostico else "N/A", style_normal)
    diagnostico_paragraph.wrapOn(c, 400, 100)
    diagnostico_paragraph.drawOn(c, 220, height - 340)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 380, "Solução Aplicada:")
    c.setFont("Helvetica", 12)
    solucao_paragraph = Paragraph(solucao if solucao else "N/A", style_normal)
    solucao_paragraph.wrapOn(c, 400, 100)
    solucao_paragraph.drawOn(c, 220, height - 400)
    
    # Valor e status
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 450, "Valor do Serviço:")
    c.setFont("Helvetica", 14)
    c.drawString(240, height - 450, f"R$ {float(valor):.2f}")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 480, "Status:")
    c.setFont("Helvetica", 14)
    c.drawString(180, height - 480, status)
    
    # Rodapé
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, 50, "Dino Tech - Sistemas & Automações")
    c.drawString(100, 30, "Email: dinotech1911@gmail.com")
    
    c.save()
    return filename