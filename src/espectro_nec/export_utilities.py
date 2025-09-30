import os
import pandas as pd
import io
from tkinter import filedialog, messagebox

def export_to_excel(T, Sa, Se, Si, zona_sismica, tipo_suelo, region, r_valor, i_valor, phi_p, phi_e):
    """
    Exporta los datos del espectro a un archivo Excel
    
    Args:
        T, Sa, Se, Si: Arrays con los datos del espectro
        zona_sismica, tipo_suelo, region: Parámetros de ubicación
        r_valor, i_valor, phi_p, phi_e: Parámetros estructurales
    """
    try:
        # Crear un DataFrame con los datos
        df = pd.DataFrame({
            'Período (s)': T,
            'Sa (g)': Sa,
            'Se (g)': Se,
            'Si (g)': Si
        })
        
        # Solicitar al usuario la ubicación para guardar el archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar espectro como Excel"
        )
        
        if not file_path:
            return  # El usuario canceló la operación
        
        # Crear un escritor de Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Hoja de datos del espectro
            df.to_excel(writer, sheet_name='Espectro', index=False)
            
            # Hoja de parámetros
            params_df = pd.DataFrame({
                'Parámetro': ['Zona Sísmica', 'Región', 'Tipo de Suelo', 'Factor R', 'Factor I', 'Factor φP', 'Factor φE'],
                'Valor': [zona_sismica, region, tipo_suelo, r_valor, i_valor, phi_p, phi_e]
            })
            params_df.to_excel(writer, sheet_name='Parámetros', index=False)
        
        messagebox.showinfo("Éxito", f"Datos exportados correctamente a {os.path.basename(file_path)}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar los datos: {str(e)}")

def save_image(fig):
    """
    Guarda la figura del espectro como una imagen
    
    Args:
        fig: Figura de matplotlib a guardar
    """
    try:
        # Solicitar al usuario la ubicación para guardar la imagen
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Guardar gráfica como imagen"
        )
        
        if not file_path:
            return  # El usuario canceló la operación
        
        # Guardar la figura
        fig.savefig(file_path, dpi=300, bbox_inches='tight')
        
        messagebox.showinfo("Éxito", f"Imagen guardada correctamente como {os.path.basename(file_path)}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar la imagen: {str(e)}")

def generate_pdf_report(T, Sa, Se, Si, zona_sismica, tipo_suelo, region, r_valor, i_valor, phi_p, phi_e, fig):
    """
    Genera un reporte PDF con los resultados del espectro sísmico
    
    Args:
        T, Sa, Se, Si: Arrays con los datos del espectro
        zona_sismica, tipo_suelo, region: Parámetros de ubicación
        r_valor, i_valor, phi_p, phi_e: Parámetros estructurales
        fig: Figura de matplotlib con el gráfico del espectro
    """
    try:
        # Verificar si reportlab está instalado
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
        except ImportError:
            messagebox.showerror("Error", "Se requiere instalar la biblioteca reportlab. Por favor ejecute 'pip install reportlab' en su terminal y reinicie la aplicación.")
            return
        
        # Calcular los parámetros para el reporte
        from .seismic_calculations import calculate_parameters
        parametros, eta, Z = calculate_parameters(tipo_suelo, zona_sismica, region)
        Fa, Fd, Fs, r = parametros['Fa'], parametros['Fd'], parametros['Fs'], parametros['r']
        
        # Calcular los puntos característicos
        T0 = 0.1 * Fs * Fd / Fa
        Tc = 0.55 * Fs * Fd / Fa
        TL = 2.4 * Fd
        
        # Solicitar al usuario la ubicación para guardar el archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Guardar reporte como PDF"
        )
        
        if not file_path:
            return  # El usuario canceló la operación
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Añadir un estilo personalizado para títulos
        styles.add(ParagraphStyle(name='TitleStyle',
                                parent=styles['Heading1'],
                                fontSize=14,
                                alignment=1,  # Centrado
                                spaceAfter=12))
        
        # Título del reporte
        elements.append(Paragraph("Reporte de Espectro de Diseño Sísmico NEC", styles['TitleStyle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Sección 1: Parámetros Iniciales
        elements.append(Paragraph("1. Parámetros Iniciales", styles['Heading2']))
        data = [
            ["Parámetro", "Valor"],
            ["Zona Sísmica", f"{zona_sismica} ({Z}g)"],
            ["Región", region],
            ["Tipo de Suelo", tipo_suelo],
            ["Factor R", str(r_valor)],
            ["Factor I", str(i_valor)],
            ["Factor φP", str(phi_p)],
            ["Factor φE", str(phi_e)]
        ]
        t = Table(data, colWidths=[2.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.2*inch))
        
        # Sección 2: Parámetros Calculados
        elements.append(Paragraph("2. Parámetros Calculados", styles['Heading2']))
        data = [
            ["Parámetro", "Valor"],
            ["Factor de amplificación (Fa)", f"{Fa:.2f}"],
            ["Factor de amplificación (Fd)", f"{Fd:.2f}"],
            ["Factor de comportamiento no lineal (Fs)", f"{Fs:.2f}"],
            ["Factor de región (η)", f"{eta:.2f}"],
            ["Período T0", f"{T0:.2f} s"],
            ["Período Tc", f"{Tc:.2f} s"],
            ["Período TL", f"{TL:.2f} s"]
        ]
        t = Table(data, colWidths=[2.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.2*inch))
        
        # Sección 3: Gráfico del Espectro
        elements.append(Paragraph("3. Gráfico de Espectros Elástico e Inelástico", styles['Heading2']))
        
        # Guardar la figura actual en un buffer con un tamaño controlado
        buf = io.BytesIO()
        # Ajustar el DPI y el tamaño de la figura para asegurar que quepa en la página
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        
        # Añadir la imagen al PDF con dimensiones controladas
        img = Image(buf)
        # Ajustar el tamaño de la imagen para que se adapte al documento
        # Limitar el ancho a 5 pulgadas (letter tiene 8.5 pulgadas de ancho)
        available_width = 5 * inch
        # Ajustar la altura proporcionalmente, pero limitar a 3.5 pulgadas
        img.drawWidth = available_width
        img.drawHeight = min(3.5 * inch, available_width * (img.imageHeight / img.imageWidth))
        elements.append(img)
        elements.append(Spacer(1, 0.2*inch))
        
        # Sección 4: Conclusiones
        elements.append(Paragraph("4. Conclusiones", styles['Heading2']))
        
        # Obtener valores máximos
        max_Sa = max(Sa)
        max_Si = max(Si)
        
        # Texto de conclusión
        conclusion_text = f"""
        El espectro de diseño sísmico ha sido generado utilizando la Norma Ecuatoriana de la Construcción (NEC).
        
        Para la zona sísmica {zona_sismica} ({Z}g) en la región {region} y con un suelo tipo {tipo_suelo}, 
        el espectro elástico alcanza una aceleración máxima de {max_Sa:.2f}g en el rango de períodos entre {T0:.2f}s y {Tc:.2f}s.
        
        El espectro inelástico, considerando un factor de reducción R={r_valor} y un factor de importancia I={i_valor}, 
        muestra una aceleración máxima de {max_Si:.2f}g.
        
        Los factores de configuración estructural utilizados fueron φP={phi_p} (en planta) y φE={phi_e} (en elevación).
        
        Este espectro debe utilizarse como base para el análisis y diseño sísmico de la estructura, 
        considerando las especificaciones y requerimientos adicionales establecidos en la NEC.
        """
        
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        
        # Finalizar y guardar el documento
        doc.build(elements)
        
        messagebox.showinfo("Éxito", f"Reporte PDF generado correctamente: {os.path.basename(file_path)}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el reporte PDF: {str(e)}")