import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .constants import (
    ZONA_SISMICA_OPTIONS,
    REGION_OPTIONS,
    TIPO_SUELO_OPTIONS,
    FACTOR_R_OPTIONS,
    FACTOR_I_OPTIONS,
)


def _labeled_combo(panel, row, text, variable, values):
    ttk.Label(panel, text=text).grid(column=0, row=row, sticky=W, pady=4)
    combo = ttk.Combobox(panel, textvariable=variable, width=40, state="readonly")
    combo["values"] = values
    combo.grid(column=1, row=row, sticky=W, columnspan=2, pady=4)
    return combo


def create_input_panel(panel, variables, generar_callback, exportar_callback, imagen_callback, pdf_callback, etabs_callback):
    """
    Crea los componentes de la interfaz de usuario en el panel izquierdo
    """
    panel.columnconfigure(1, weight=1)

    title = "Espectro Sísmico NEC · v0.2 · CodeNormative"
    ttk.Label(panel, text=title, font=("Helvetica", 13, "bold")).grid(
        column=0, row=0, columnspan=3, sticky=W, pady=(0, 18)
    )

    _labeled_combo(panel, 1, "Zona Sísmica (Z):", variables["zona_sismica_var"], ZONA_SISMICA_OPTIONS)
    _labeled_combo(panel, 2, "Región:", variables["region_var"], REGION_OPTIONS)
    _labeled_combo(panel, 3, "Tipo de Suelo:", variables["tipo_suelo_var"], TIPO_SUELO_OPTIONS)
    _labeled_combo(panel, 4, "Factor R:", variables["r_var"], FACTOR_R_OPTIONS)
    _labeled_combo(panel, 5, "Factor I:", variables["i_var"], FACTOR_I_OPTIONS)

    ttk.Label(panel, text="Factor ØP:").grid(column=0, row=6, sticky=W, pady=4)
    ttk.Entry(panel, textvariable=variables["phi_p_var"], width=12).grid(column=1, row=6, sticky=W, pady=4)
    ttk.Label(panel, text="(Configuración en planta)").grid(column=2, row=6, sticky=W, padx=5, pady=4)

    ttk.Label(panel, text="Factor ØE:").grid(column=0, row=7, sticky=W, pady=4)
    ttk.Entry(panel, textvariable=variables["phi_e_var"], width=12).grid(column=1, row=7, sticky=W, pady=4)
    ttk.Label(panel, text="(Configuración en elevación)").grid(column=2, row=7, sticky=W, padx=5, pady=4)

    botones_frame = ttk.Frame(panel)
    botones_frame.grid(column=0, row=8, columnspan=3, pady=14, sticky=W)

    ttk.Button(botones_frame, text="Generar Espectro", command=generar_callback, bootstyle="primary").grid(
        column=0, row=0, padx=(0, 5)
    )
    
    export_menu = ttk.Menubutton(botones_frame, text="Exportar", bootstyle="info")
    export_menu.grid(column=1, row=0, padx=5)
    
    menu = ttk.Menu(export_menu)
    menu.add_command(label="Exportar a Excel", command=exportar_callback)
    menu.add_command(label="Exportar a ETABS (.txt)", command=etabs_callback)
    menu.add_command(label="Guardar Gráfico (.png)", command=imagen_callback)
    menu.add_separator()
    menu.add_command(label="Generar Reporte PDF", command=pdf_callback)
    export_menu['menu'] = menu
    
    info_frame = ttk.Labelframe(panel, text="Información", padding="10 10 10 10")
    info_frame.grid(column=0, row=9, columnspan=3, sticky=(W, E), pady=10)

    info_text = (
        "Este programa genera el espectro de diseño sísmico según la NEC.\n"
        "Los valores de R deben seleccionarse según el sistema estructural.\n"
        "Los valores de I deben seleccionarse según el tipo de uso o importancia de la estructura.\n\n"
        "Fuente: Ing. Vinces Mendoza Maikel Andres - CodeNormative v.0.2"
    )

    ttk.Label(info_frame, text=info_text, wraplength=360).grid(column=0, row=0, sticky=W)