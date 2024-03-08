# ===========================================================================
# Importaciones de clases y librerias necesarias en esta vista
# ===========================================================================
# Region - Importación de librerias y clases.
import pandas as pd
import easygui as eg
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar, messagebox

from controller.Ejecucion import Ejecucion
from controller.utils.Helpers import Helpers
# Endregion - Importación de librerias y clases.

# Region - Inicialización de clases para uso de metodos.
ejec = Ejecucion()
helpers = Helpers()
# Endregion - Inicialización de clases para uso de metodos.

class VentanaPrincipalForm:
    """
    VentanaPrincipalForm
    ====================
    Clase para gestionar la creación del formulario
    de ttk, con estilos personalizados para el proceso
    de armado de cuentas del proyecto zentria.
    """
    def __init__(self):
        self.__preInitBase = []

        # Region - Configuración de ventana (Form)
        self.ventana = tk.Tk()  # Instancia de Tkinter en var ventana

        super().__init__()                        
        self.ventana.title('Armado Cuentas Zentria V1.0.0.0') # Titulo de la ventana
        self.ventana.geometry('800x500') # Dimensiones iniciales de la ventana
        self.ventana.config(bg='#FFF3F1') # Fondo de la ventana
        self.ventana.resizable(width=0, height=0) # Inhabilita el resize de la ventana por usuario
        helpers.centerWindows(self.ventana,450,860) # height | width Se centra la ventana en pantalla
        style = ttk.Style(self.ventana) # Se le asignan estilos desde una var a la ventana
        self.ventana.tk.call("source", "forest-light.tcl") # Importación de los estilos, desde un theme
        style.theme_use("forest-light") # Instancia del theme desde la variable Style
        logo = helpers.getImage("IconPrincipal", (200, 200)) # Logo de aplicativo
        self.ventana.iconphoto(True, logo)
        # Endregion - Configuración de ventana (Form)
        
        # Region - Variables globales a usar dentro del form
        typeCase = StringVar() # Asignación de tipo a una variable
        combo_list = ["-- Selecciona EPS --", "NuevaEPS"] # Lista de datos a seleccionar
        self.dfExcel = ""
        # Endregion - Variables globales a usar dentro del form
        
        # region Metodos internos
        def setTypeCase(e):
            proceso = typeCase.get()
            if proceso == "-- Selecciona EPS --":
                helpers.SetInfoDisabled(txtSeleccionadaEPS, "Aun no tienes selecionada una opción")
            else:
                epsSeleccionada = proceso
                helpers.SetInfoDisabled(txtSeleccionadaEPS, f"EPS --> {str(proceso)}")
        
        # Lectura de excel para pre iniciliazación de datos en vista
        def preInitData(ruta):
            df = pd.read_excel(ruta)
            totalAtenciones = len(df["numero_atencion"].to_list())
            totalFacturas = len(df["numero_factura"].to_list())
            diferenciaAtenciones = int(totalAtenciones) - int(totalFacturas)
            self.dfExcel = df
            helpers.SetInfoDisabled(txtNumCuentas, f"{totalAtenciones}")
            helpers.SetInfoDisabled(txtNumFacturas, f"{totalFacturas}")
            helpers.SetInfoDisabled(txtDiferencia, f"Diferencia entre totales: {diferenciaAtenciones}")
        
        # Metodo para validar los campos para ejecutar el proceso
        def validatefields():
            if txtSeleccionadaEPS.get() == "Aún no tienes selecionada una [EPS]":
                messagebox.showinfo(message="No has seleccionado una EPS aún", title = "¡ERROR!")
            elif txtArchivoCuentas.get() == "Aun no tienes selecionada un [Archivo Base] de cuentas a procesar":
                messagebox.showinfo(message="No has seleccionado aún un excel con cuentas para armar", title = "¡ERROR!")
            elif txtFechaRadicado.get() == "":                    
                messagebox.showinfo(message="Debes especificar una fecha de radicado en la cuál buscar soportes. (Ejem: 20240315)", title = "¡ERROR!")
            elif(txtFechaRadicado.get().isnumeric() is not True):
                messagebox.showinfo(message = f"La fecha de radicado ingresada: [{txtFechaRadicado.get()}] no es valida, recuerda que solo pueden ser números.\n¡Ejem: (20240315) Año, luego mes, luego día!", title = "¡ERROR!")
            elif txtNumeroRadicado.get() == "":
                messagebox.showinfo(message="No has especificado el radicado para el armado de cuentas", title = "¡ERROR!")
            else:
                return True

        # Metodo generico para traer la unformacion de rutas escogidas dependiendo el btn ejecutado
        def getRoute(typeBtn):
            try:
                if typeBtn == "ExcelCuentas": # el typebtn trae el valor enviado por parametro
                    ruta = eg.fileopenbox(msg = "Selecciona el archivo de cuentas", title = "Excel cuentas", filetypes = ["*.xlsx"])
                    helpers.SetInfoDisabled(txtArchivoCuentas, ruta)
                    preInitData(ruta) # Setea la información en vista del excel.
                    messagebox.showinfo(message="Archivo de cuentas para armado, cargadó con éxito." , title="Mensaje de alerta")
                    return ruta
            except Exception  as e: # Si hay alguna exception instanciamos los valores a vacio.
                if typeBtn == "ExcelCuentas":
                    helpers.SetInfoDisabled(txtArchivoCuentas,"Aun no tienes selecionada un [Archivo Base] de cuentas a procesar")
                    helpers.SetInfoDisabled(txtNumCuentas, "0")
                    helpers.SetInfoDisabled(txtNumFacturas, "0")
                    helpers.SetInfoDisabled(txtDiferencia, "0")
                    messagebox.showinfo(message = f"Error en la carga de archivo, error: {str(e)}, contacta a soporte.",title = "¡ERROR!")
                else:
                    # print(str(e))
                    messagebox.showinfo(message="Error: " + str(e),title = "¡ERROR!")

        # Metodo para ejecutar el procesos principal
        def Execute(): 
            try:
                if validatefields():
                    continuar = messagebox.askyesno(message="¿Estás seguro de ejecutar el proceso?", title = "Espera...")
                    if(continuar):
                        ejec.dataRadicarFecha = txtFechaRadicado.get()
                        ejec.dataRadicarNumero = txtNumeroRadicado.get()
                        ejec.dataRadicarDaFram = self.dfExcel.to_json(orient ='index') 
                        ejec.dataRadicarEPS = typeCase.get()
                        dataCargada = ejec.cargarDataBaseDatos() # Metodo de la clase encargado de subir información a base de datos.
                        if(dataCargada):
                            messagebox.showinfo(message = "Se ha iniciado la ejecución con éxito, ya puedes cerrar esta ventana.", title = "¡Éxito!")
                        else:
                            messagebox.showerror(message = "Ocurrió un error cargando los datos a base de datos de armado, consulta a soporte.", title = "¡ERROR!")
            except Exception  as e:
                messagebox.showinfo(message = f"No ha sido posible realizar la ejecución, valida con soporte. Error: {str(e)}", title = "¡ERROR!")

        # Endregion Metodos internos
        

        # Region - Header del formulario.
        # =========================================================================
        # | Frame - Header completo
        # =========================================================================
        frameHeader = tk.Frame(self.ventana, bd = 0, height = 100, relief = tk.SOLID, padx = 1, pady = 1,bg = '#fcfcfc')
        frameHeader.pack(side = "top", expand = tk.FALSE, fill = tk.BOTH)
        
        # Region - Left side Header
        # =========================================================================
        # | Frame Left side Header
        # =========================================================================
        frameLeftHeader = tk.Frame(frameHeader, bd = 0, relief = tk.SOLID, bg = '#F1F1F1', width = 400)
        frameLeftHeader.pack(side = "left", expand = tk.FALSE, fill = tk.BOTH)
        # Configuración de logo de Yawi
        logoYawi = helpers.getImage("LogoYawi", (400, 70))
        label = tk.Label(frameLeftHeader, image = logoYawi, bg = "#EBEBEB")
        label.place( x = 0, y = 0, relwidth = 1, relheight = 1)
        # Endregion - Left side Header
        
        # Region Right side Header
        # =========================================================================
        # | Frame Right side Header
        # =========================================================================
        frameRightHeader  = tk.Frame(frameHeader, height = 100, bd = 0, relief = tk.SOLID, bg = '#F1F1F1')
        frameRightHeader.pack(side = "right", expand = tk.YES, fill = tk.BOTH)
        # Configuración del titulo del formulario
        title = tk.Label(frameRightHeader, text = "Armado Zentria", font = ('Times', 40), fg = "#217346", bg = '#EBEBEB', pady=20)
        title.pack(expand = tk.FALSE, fill = tk.BOTH)
        # Endregion Right side Header
        # Endregion - Header del formulario.

        # Region - Cuerpo principal del formulario        
        # Region rightbody
        # =========================================================================
        # | frame form campos y botones
        # =========================================================================
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.TRUE,fill=tk.BOTH)
        
        # =========================================================================
        # | Frame Left Body
        # =========================================================================
        frameLeft = tk.Frame(frame_form, bd = 0, relief = tk.SOLID, bg = '#fcfcfc', padx = 20, pady = 0)
        frameLeft.pack(side = "left", expand = tk.YES, fill = tk.BOTH)
        
        # Label para ComboBox
        lblArmadoEPS = ttk.Label(frameLeft, text="EPS de armado de cuenta:",font=('Times', 10),background='#fcfcfc', width=25)
        lblArmadoEPS.grid(row = 0, column = 0, padx = 0, pady = (10, 2),  sticky = "ew")
        
        # ComboBox seleccionar EPS
        typeCase = ttk.Combobox(frameLeft, values = combo_list, width = 30)
        typeCase.current(0)
        typeCase.grid(row = 1, column = 0, padx = 0, pady = 2,  sticky = "ew")
        typeCase.bind("<<ComboboxSelected>>", setTypeCase)
        
        # Label para cantidad de cuentas y facturas encontradas
        lblCuentasFacturas = ttk.Label(frameLeft, text = "N° de cuentas armar     /  N° de facturas", font = ('Times', 10),
                                background = '#fcfcfc', width = 25)
        lblCuentasFacturas.grid(row = 2, column = 0, padx = 0, pady = (10, 2), sticky = "ew")
        
        # =========================================================================
        # | Frame para campos de información 
        # =========================================================================
        frameNumber = tk.Frame(frameLeft, bd = 0, relief = tk.SOLID, bg = '#fcfcfc', padx = 0, pady = 0)
        frameNumber.grid(row = 3, column = 0, padx = 0, pady = 0, sticky = "ew")
        
        # Cuadro de texto para número de cuentas para armar
        txtNumCuentas = ttk.Entry(frameNumber, width = 15)
        txtNumCuentas.grid(row = 3, column = 0, padx = 0, pady = (0, 0), sticky = "w")
        txtNumCuentas.insert(0,"0")
        txtNumCuentas.configure(state = 'disabled')

        # Cuadro de texto para número de facturas reportadas por cuenta
        txtNumFacturas = ttk.Entry(frameNumber, width = 15)
        txtNumFacturas.grid(row = 3, column = 1, padx = (10, 0), pady = (0, 0), sticky = "w")
        txtNumFacturas.insert(0, "0")
        txtNumFacturas.configure(state = 'disabled')
        
        # Label informativo para número de diferencia entre facturas y cuentas
        lblDiferencia = ttk.Label(frameLeft, text = "Diferencia entre facturas y cuentas", font = ('Times', 10),
                                background = '#fcfcfc', width = 25)
        lblDiferencia.grid(row = 4, column = 0, padx = 5, pady = (10,2),  sticky = "ew")
        
        # Cuadro de texto para diferencia entre facturas y cuentas.
        txtDiferencia = ttk.Entry(frameLeft, width = 25)
        txtDiferencia.grid(row = 5, column = 0, padx = 0, pady = (0, 10), sticky = "ew")
        txtDiferencia.insert(0, "0")
        txtDiferencia.configure(state = 'disabled')
        
        # =========================================================================
        # | Frame Left Radio Buttons
        # =========================================================================
        frameRadios = tk.Frame(frameLeft, bd = 0, relief = tk.SOLID, bg = '#fcfcfc', padx = 0, pady = 0)
        frameRadios.grid(row = 6, column = 0, padx = 0, pady = (10,20), sticky = "ew")
        checkFolder = tk.IntVar(value = 1)
        checkExcell = tk.IntVar(value = 1)
        
        # Label informativo tipo de proceso
        lblTipoProceso = ttk.Label(frameRadios, text = "Selecciona un proceso", font = ('Times', 10),
                                background = '#fcfcfc', width = 25)
        lblTipoProceso.grid(row = 6, column = 0, padx = 5, pady = (10,2),  sticky = "nsew")
        
        # Radio Buttons tipo de proceso
        radioUno = ttk.Radiobutton(frameRadios, text = "Armar Cuentas", variable = checkExcell, value = 1)
        radioUno.grid(row = 7, column = 0, padx = 0, pady = (0, 9), sticky = "nsew")
        radioDos = ttk.Radiobutton(frameRadios, text = "¿Otro...?", variable = checkExcell, value = 2)
        radioDos.grid(row = 7, column = 1, padx = 0, pady = (0, 9), sticky = "nsew")
        
        # Accentbutton Ejecutar Proceso Total
        btnEjecutarProceso = ttk.Button(frameLeft, text = "Ejecutar Proceso Seleccionado",
                                style = "Accent.TButton", command = Execute)
        btnEjecutarProceso.grid(row = 8, column = 0, padx = 0, pady = 10, sticky = "ew")

        # =========================================================================
        # | Frame Left Body
        # =========================================================================
        frameRight = tk.Frame(frame_form, bd=0, relief=tk.SOLID,bg='#fcfcfc',padx=30, pady=10)
        frameRight.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        
        # Label EPS seleccionada en proceso
        lblSeleecionadaEPS = ttk.Label(frameRight, text="EPS seleccionada a procesar:",font=('Times', 10), background='#fcfcfc')
        lblSeleecionadaEPS.grid(row=0, column=0, padx=2, pady=0, sticky="w")
        
        # Cuadro de texto de EPS seleccionada en proceso
        txtSeleccionadaEPS = ttk.Entry(frameRight, width=70)
        txtSeleccionadaEPS.grid(row=1, column=0, padx=0, pady=(2, 10), sticky="ew")
        txtSeleccionadaEPS.insert(0,"Aún no tienes selecionada una [EPS]")
        txtSeleccionadaEPS.configure(state='disabled')
        
        # Label archivo de cuentas a procesar
        lblArchivoCuentas = ttk.Label(frameRight, text="Archivo base de cuentas a procesar",font=('Times', 10),background='#fcfcfc')
        lblArchivoCuentas.grid(row=2, column=0, padx=2, pady=0, sticky="w")
        
        # Cuadro de texto del archivo de cuentas a procesar
        txtArchivoCuentas = ttk.Entry(frameRight, width=70)
        txtArchivoCuentas.grid(row=3, column=0, padx=0, pady=(2, 10), sticky="ew")
        txtArchivoCuentas.insert(0,"Aun no tienes selecionada un [Archivo Base] de cuentas a procesar")
        txtArchivoCuentas.configure(state='disabled')
        
        # Label Fecha del radicado
        lblFechaRadicado = ttk.Label(frameRight, text="Fecha del radicado a procesar [20240315]",font=('Times', 10),background='#fcfcfc')
        lblFechaRadicado.grid(row=4, column=0, padx=2, pady=0, sticky="w")
        
        # Cuadro de texto de la fecha del radicado
        txtFechaRadicado = ttk.Entry(frameRight, width=70)
        txtFechaRadicado.grid(row=5, column=0, padx=0, pady=(2, 10), sticky="ew")
        txtFechaRadicado.insert(0,"")
        
        # Label para el número de Radicado
        lblRouteFolders = ttk.Label(frameRight, text="Escribe el Radicado como lo genera el software [RAD-12345]",font=('Times', 10),background='#fcfcfc')
        lblRouteFolders.grid(row=6, column=0, padx=2, pady=0, sticky="w")
        
        # Cuadro de texto para el número del radicado
        txtNumeroRadicado = ttk.Entry(frameRight, width=70)
        txtNumeroRadicado.grid(row=7, column=0, padx=0, pady=(2, 15), sticky="ew")
        txtNumeroRadicado.insert(0,"")

        frameBtns = tk.Frame(frameRight, bd=0, relief=tk.SOLID,bg='#fcfcfc', padx=0, pady=5)
        frameBtns.grid(row=8, column=0, padx=0, pady=0,  sticky="ew")
        
        # Accentbutton
        # btnDataBase = ttk.Button(frameBtns, text="Seleccionar Base de Datos",style="Accent.TButton",
        #                          width=32, command=lambda: getRoute("ExcelCuentas"))
        # btnDataBase.grid(row=8, column=0, padx=(0,5), pady=0, sticky="ew")
        
        # btnRouteDestiny = ttk.Button(frameBtns, text="Seleccionar Ruta de Destino", style="Accent.TButton",
        #                              width=32,command=lambda: getRoute("RouteDestiny"))
        # btnRouteDestiny.grid(row=8, column=1, padx=(5,0), pady=0, sticky="ew")
        
         # Accentbutton
        btnContratos = ttk.Button(frameBtns, text="Selecciona archivo de excel (xlsx) con datos de cuentas.",
                                 style="Accent.TButton", width=70, command=lambda: getRoute("ExcelCuentas"))
        btnContratos.grid(row=9, column=0, columnspan=2, padx=0, pady=10)
        
        # endregion rightbody
        # Endregion  - Cuerpo principal del formulario 
        self.ventana.mainloop()

# Metodo para inicializar el metodo ventana principal    
if __name__ == '__main__':
    VentanaPrincipalForm()