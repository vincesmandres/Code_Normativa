import os
import io
import pandas as pd
import numpy as np
from tkinter import filedialog
from ttkbootstrap.dialogs import Messagebox


SOURCE_FOOTER = "Fuente: Ing. Vinces Mendoza Maikel Andres - CodeNormative v.0.2"


def export_to_etabs(T, Si):
    """
    Exporta el espectro inelástico a un archivo de texto compatible con ETABS.
    El formato es: Período (s) vs Aceleración (g)
    """
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Guardar espectro para ETABS",
        )

        if not file_path:
            return

        # ETABS requiere los datos en un formato de dos columnas: Periodo, Aceleracion
        # Los datos se guardan separados por espacios
        export_data = np.vstack((T, Si)).T
        
        # Agregar el punto (0, Si[0]) que ETABS requiere
        initial_point = np.array([[0, Si[0]]])
        export_data = np.vstack((initial_point, export_data))

        np.savetxt(file_path, export_data, fmt="%.4f", delimiter="    ", header="Espectro Sismico", comments="")

        Messagebox.showinfo("Éxito", f"Datos para ETABS exportados correctamente a {os.path.basename(file_path)}")

    except Exception as e:
        Messagebox.showerror("Error", f"Error al exportar los datos para ETABS: {str(e)}")


def export_to_excel(T, Sa, Se, Si, zona_sismica, tipo_suelo, region, r_valor, i_valor, phi_p, phi_e):
    """
    Exporta los datos del espectro a un archivo Excel
    """
    try:
        df = pd.DataFrame(
            {
                "Periodo (s)": T,
                "Sa (g)": Sa,
                "Se (g)": Se,
                "Si (g)": Si,
            }
        )

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar espectro como Excel",
        )

        if not file_path:
            return

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Espectro", index=False)

            params_df = pd.DataFrame(
                {
                    "Parámetro": [
                        "Zona Sísmica",
                        "Región",
                        "Tipo de Suelo",
                        "Factor R",
                        "Factor I",
                        "Factor ØP",
                        "Factor ØE",
                        "Fuente",
                    ],
                    "Valor": [
                        zona_sismica,
                        region,
                        tipo_suelo,
                        r_valor,
                        i_valor,
                        phi_p,
                        phi_e,
                        SOURCE_FOOTER,
                    ],
                }
            )
            params_df.to_excel(writer, sheet_name="Parámetros", index=False)

        Messagebox.showinfo("Éxito", f"Datos exportados correctamente a {os.path.basename(file_path)}")

    except Exception as e:
        Messagebox.showerror("Error", f"Error al exportar los datos: {str(e)}")


def save_image(fig):
    """
    Guarda la figura del espectro como una imagen
    """
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Guardar gráfica como imagen",
        )

        if not file_path:
            return

        fig.savefig(file_path, dpi=300, bbox_inches="tight")

        Messagebox.showinfo("Éxito", f"Imagen guardada correctamente como {os.path.basename(file_path)}")

    except Exception as e:
        Messagebox.showerror("Error", f"Error al guardar la imagen: {str(e)}")


def generate_pdf_report(T, Sa, Se, Si, zona_sismica, tipo_suelo, region, r_valor, i_valor, phi_p, phi_e, fig):
    """
    Genera un reporte PDF con un diseño mejorado.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Frame, PageTemplate
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.colors import HexColor

        # Colores y Estilos
        primary_color = HexColor("#1f6feb")
        secondary_color = HexColor("#0d1117")
        text_color = HexColor("#e6edf3")
        bg_color = HexColor("#f6f8fa")

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TitleStyle', fontSize=18, alignment=1, spaceAfter=20, textColor=secondary_color))
        styles.add(ParagraphStyle(name='HeaderStyle', fontSize=14, spaceAfter=12, textColor=primary_color))
        styles.add(ParagraphStyle(name='BodyStyle', fontSize=10, leading=14, textColor=secondary_color))
        styles.add(ParagraphStyle(name='FooterStyle', fontSize=8, alignment=1, textColor=colors.grey))

        # --- Creación del PDF ---
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Guardar reporte como PDF",
        )
        if not file_path:
            return

        doc = SimpleDocTemplate(file_path, pagesize=letter, topMargin=1.5*inch, bottomMargin=1*inch)
        
        # --- Cabecera y Pie de Página ---
        def header(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(primary_color)
            canvas.rect(doc.leftMargin, doc.height + 0.7*inch, doc.width, 0.5*inch, fill=1, stroke=0)
            
            # --- Placeholder para el logo ---
            # Reemplazar 'logo.png' con la ruta a un logo real
            logo_path = "logo.png" 
            if os.path.exists(logo_path):
                canvas.drawImage(logo_path, doc.leftMargin + 0.1*inch, doc.height + 0.8*inch, 
                                 width=0.6*inch, height=0.6*inch, mask='auto')
            
            canvas.setFillColor(colors.white)
            canvas.setFont('Helvetica-Bold', 16)
            canvas.drawCentredString(doc.width/2 + doc.leftMargin, doc.height + 0.95*inch, "Reporte de Diseño Sísmico")
            canvas.restoreState()

        def footer(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(colors.grey)
            footer_text = f"Página {doc.page} | {SOURCE_FOOTER}"
            canvas.drawCentredString(doc.width/2 + doc.leftMargin, 0.5 * inch, footer_text)
            canvas.restoreState()

        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        template = PageTemplate(id='main_template', frames=[frame], onPage=header, onPageEnd=footer)
        doc.addPageTemplates([template])

        elements = []
        
        # --- Contenido ---
        from .seismic_calculations import calculate_parameters
        parametros, eta, Z = calculate_parameters(tipo_suelo, zona_sismica, region)
        Fa, Fd, Fs, r = parametros["Fa"], parametros["Fd"], parametros["Fs"], parametros["r"]
        T0, Tc, TL = 0.1 * Fs * Fd / Fa, 0.55 * Fs * Fd / Fa, 2.4 * Fd

        elements.append(Paragraph("1. Parámetros de Entrada", styles['HeaderStyle']))
        
        param_data = [
            ['Zona Sísmica:', f"{zona_sismica} ({Z}g)", 'Región:', region],
            ['Tipo de Suelo:', tipo_suelo, 'Factor R:', f"{r_valor:.2f}"],
            ['Factor I:', f"{i_valor:.2f}", 'Factor ØP:', f"{phi_p:.2f}"],
            ['Factor ØE:', f"{phi_e:.2f}", '', '']
        ]
        param_table = Table(param_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        param_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), secondary_color),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), bg_color),
            ('BACKGROUND', (2, 0), (2, -1), bg_color),
        ]))
        elements.append(param_table)
        elements.append(Spacer(1, 0.2*inch))

        elements.append(Paragraph("2. Parámetros Sísmicos Calculados (NEC)", styles['HeaderStyle']))
        calc_param_data = [
            ['Fa:', f"{Fa:.3f}", 'Fd:', f"{Fd:.3f}", 'Fs:', f"{Fs:.3f}"],
            ['η:', f"{eta:.3f}", 'T0 (s):', f"{T0:.3f}"],
            ['Tc (s):', f"{Tc:.3f}", 'TL (s):', f"{TL:.3f}"]
        ]
        calc_param_table = Table(calc_param_data, colWidths=[2*inch, 1*inch, 2*inch, 1*inch])
        calc_param_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
             ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ]))
        elements.append(calc_param_table)
        elements.append(Spacer(1, 0.2*inch))

        elements.append(Paragraph("3. Gráfico del Espectro de Diseño", styles['HeaderStyle']))
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        img = Image(buf, width=6*inch, height=4*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("4. Tabla de Datos del Espectro", styles['HeaderStyle']))
        
        # Crear tabla de datos del espectro
        max_rows = 20
        step = max(1, len(T) // max_rows)
        spectrum_data = [['Período (s)', 'Sa (g)', 'Se (g)', 'Si (g)']]
        for i in range(0, len(T), step):
            spectrum_data.append([f"{T[i]:.3f}", f"{Sa[i]:.4f}", f"{Se[i]:.4f}", f"{Si[i]:.4f}"])
            
        spectrum_table = Table(spectrum_data)
        spectrum_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), primary_color),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), bg_color),
            ('GRID', (0,0), (-1,-1), 1, colors.grey)
        ]))
        elements.append(spectrum_table)
        
        doc.build(elements)
        Messagebox.showinfo("Éxito", f"Reporte PDF mejorado generado correctamente en: {os.path.basename(file_path)}")

    except Exception as e:
        Messagebox.showerror("Error", f"Error al generar el reporte PDF: {str(e)}")
