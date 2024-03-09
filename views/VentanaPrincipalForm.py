# ===========================================================================
# Importaciones de clases y librerias necesarias en esta vista
# ===========================================================================
# Region - Importación de librerias y clases.
import tkinter as tk
from tkinter import ttk
from itertools import groupby
from tkinter import StringVar, messagebox

from controller.Ejecucion import Ejecucion
from controller.Peticiones import Peticiones
from controller.utils.Helpers import Helpers
# Endregion - Importación de librerias y clases.

# Region - Inicialización de clases para uso de metodos.
ejec = Ejecucion()
req = Peticiones()
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
        # Region - Configuración de ventana (Form)
        self.ventana = tk.Tk()  # Instancia de Tkinter en var ventana

        super().__init__()                        
        self.ventana.title('Radicación Zentria - V1.0.0.0') # Titulo de la ventana
        self.ventana.geometry('800x500') # Dimensiones iniciales de la ventana
        self.ventana.config(bg = '#FFF3F1') # Fondo de la ventana
        self.ventana.resizable(width = 0, height = 0) # Inhabilita el resize de la ventana por usuario
        helpers.centerWindows(self.ventana, 450, 860) # height | width Se centra la ventana en pantalla
        style = ttk.Style(self.ventana) # Se le asignan estilos desde una var a la ventana
        self.ventana.tk.call("source", "forest-light.tcl") # Importación de los estilos, desde un theme
        style.theme_use("forest-light") # Instancia del theme desde la variable Style
        logo = helpers.getImage("IconPrincipal", (200, 200)) # Logo de aplicativo
        self.ventana.iconphoto(True, logo)
        # Endregion - Configuración de ventana (Form)
        
        # Region - Variables globales a usar dentro del form
        self.__dataSedes = req.obtenerSedes()
        # En caso de no obtener datos, se debe cerrar.        
        if(len(self.__dataSedes) == 0):
            messagebox.showinfo(message = "No se ha podido obtener la información de las sedes para Zentria.", title = "¡ERROR!")
            return
        
        # Función para obtener la clave de agrupación por cada dato de la respuesta de la API
        def agrupacionDict(dictAgrupar: dict):
            return (dictAgrupar["nombre_ips"], dictAgrupar["nombre_eps"], dictAgrupar["nit_eps"])

        agrupar = groupby(self.__dataSedes, agrupacionDict) # Agrupación de las sedes
        self.__dataAgrupadaSedes = [] # Lista seteada con la info de las sedes

        for k, grupo in agrupar:
            nombreIPS, nombreEPS, nitEPS = k # Obtención de data según key del diccionario.
            dictActual = { "nombreIPS": nombreIPS, "nombreEPS": nombreEPS, "nitEPS": nitEPS, "contratos": [] }
           
            for diccionario in grupo: # Busqueda de contratos por cada una de las iteraciones
                dictActual["contratos"].append(diccionario["nombre_contrato"])
            self.__dataAgrupadaSedes.append(dictActual) # Agregar el diccionario actual a la lista de data seteada
        
        self.__listadoIPS = [dato["nombreIPS"] for dato in self.__dataAgrupadaSedes]
        self.__listadoEPS = [dato["nombreEPS"] for dato in self.__dataAgrupadaSedes]

        self.__listadoContratos = []
        for sede in self.__dataAgrupadaSedes:
            self.__listadoContratos += sede["contratos"]

        self.__listadoIPS.insert(0, "-- Selecciona una IPS --") # Se les añade una opción por Deafult
        self.__listadoEPS.insert(0, "-- Selecciona una EPS --") # Se les añade una opción por Deafult
        self.__listadoContratos.insert(0, "-- Selecciona un Contrato --") # Se les añade una opción por Deafult
        self.__listadoRegimen = ["-- Selecciona un Regimen --", "Subsidiado", "Contributivo"]
        self.__listadoSegmentos = ["-- Selecciona un segmetno de ejecución --", "1) Generar RIPS", "2) Reprocesar RIPS", "3) Cargar Soportes"]

        tipoIPS = StringVar() # Asignación de tipo a una variable
        tipoEPS = StringVar() # Asignación de tipo a una variable
        tipoContrato = StringVar() # Asignación de tipo a una variable
        tipoRegimen = StringVar() # Asignación de tipo a una variable
        tipoSegmento = StringVar() # Asignación de tipo a una variable

        self.dfExcel = ""
        # Endregion - Variables globales a usar dentro del form
        
        # region Metodos internos
        def setTipoSeleccion(e):
            contrato = tipoContrato.get()
            regimen = tipoRegimen.get()
            if("Selecciona" in contrato or "Selecciona" in regimen):
                helpers.SetInfoDisabled(txtInfoProceso, "Configura todo el proceso.")
            else:
                helpers.SetInfoDisabled(txtInfoProceso, f"CONTRATO: {contrato}, REGIMEN: {regimen}")
                
        # Metodo para validar los campos para ejecutar el proceso
        def validatefields():
            print(txtFechaProceso.get())
            print(txtRelacionEnvio.get())
            if("Selecciona" in tipoIPS.get()):
                messagebox.showwarning(message = "No has seleccionado una [IPS] aún", title = "¡ERROR!")
                return False
            if("Selecciona" in tipoEPS.get()):
                messagebox.showwarning(message = "No has seleccionado una [EPS] aún", title = "¡ERROR!")
                return False
            if("Selecciona" in tipoContrato.get()):
                messagebox.showwarning(message = "No has seleccionado un [CONTRATO] aún", title = "¡ERROR!")
                return False
            if("Selecciona" in tipoRegimen.get()):
                messagebox.showwarning(message = "No has seleccionado un [REGIMEN] aún", title = "¡ERROR!")
                return False
            if("Selecciona" in tipoSegmento.get()):
                messagebox.showwarning(message = "No has seleccionado un [SEGMENTO] aún", title = "¡ERROR!")
                return False
            if "Selecciona" not in tipoSegmento.get() and "RIPS" in tipoSegmento.get() and (txtFechaProceso.get() == "" or txtRelacionEnvio.get() == ""):
                messagebox.showerror(message = f"Has seleccionado como segmento: [-- {tipoSegmento.get()} --].\n\nPero no has configurado correctamente los datos para fecha y relación de envío.", title = "¡ERROR!")
                return False
            else:
                return True

        # Metodo para ejecutar el procesos principal
        def Execute(): 
            try:
                print(f"validatefields() == {validatefields()}")
                if validatefields():
                    continuar = messagebox.askyesno(message="¿Estás seguro de ejecutar el proceso?", title = "Espera...")
                    if(continuar):
                        ejec.formIPS = tipoIPS.get()
                        ejec.formEPS = tipoEPS.get()
                        ejec.formCotnrato = tipoContrato.get()
                        ejec.formRegimen = tipoRegimen.get()
                        ejec.formSegmento = tipoSegmento.get()
                        ejec.formFecha = txtFechaProceso.get()
                        ejec.formValidacion = txtRelacionEnvio.get()
                        validacion = ejec.orquestarEjecucion()
                        if(validacion):
                            messagebox.showinfo(message = "Se ha iniciado la ejecución con éxito, ya puedes cerrar esta ventana.", title = "¡Éxito!")
                        else:
                            messagebox.showerror(message = "Ocurrió un error con la ejecución, contacta a soporte.", title = "¡ERROR!")
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
        title = tk.Label(frameRightHeader, text = "Radicación Zentria", font = ('Times', 40), fg = "#217346", bg = '#EBEBEB', pady=20)
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
        lblRadicacionIPS = ttk.Label(frameLeft, text = "IPS del proceso actual:", font = ('Times', 12), background = '#fcfcfc', width = 25)
        lblRadicacionIPS.grid(row = 0, column = 0, padx = 0, pady = (10, 2),  sticky = "ew")
        
        # ComboBox seleccionar IPS
        tipoIPS = ttk.Combobox(frameLeft, values = self.__listadoIPS, width = 30)
        tipoIPS.current(0)
        tipoIPS.grid(row = 1, column = 0, padx = 0, pady = 2,  sticky = "ew")
        tipoIPS.bind("<<ComboboxSelected>>", setTipoSeleccion)
        
        # Label para ComboBox
        lblRadicacionEPS = ttk.Label(frameLeft, text = "EPS para proceso de radicación:", font = ('Times', 12), background = '#fcfcfc', width = 25)
        lblRadicacionEPS.grid(row = 2, column = 0, padx = 0, pady = (10, 2),  sticky = "ew")
        # ComboBox seleccionar EPS
        tipoEPS = ttk.Combobox(frameLeft, values = self.__listadoEPS, width = 30, font = ('Times', 7))
        tipoEPS.current(0)
        tipoEPS.grid(row = 3, column = 0, padx = 0, pady = 2,  sticky = "ew")
        tipoEPS.bind("<<ComboboxSelected>>", setTipoSeleccion)

        # Label para ComboBox
        lblRadicacionContrato = ttk.Label(frameLeft, text = "Selecciona uno de los contrato:", font = ('Times', 12), background = '#fcfcfc', width = 25)
        lblRadicacionContrato.grid(row = 4, column = 0, padx = 0, pady = (10, 2),  sticky = "ew")
        # ComboBox seleccionar el contrato con la EPS
        tipoContrato = ttk.Combobox(frameLeft, values = self.__listadoContratos, width = 30, font = ('Times', 7))
        tipoContrato.current(0)
        tipoContrato.grid(row = 5, column = 0, padx = 0, pady = 2,  sticky = "ew")
        tipoContrato.bind("<<ComboboxSelected>>", setTipoSeleccion)

        # Label para ComboBox
        lblRadicacionRegimen = ttk.Label(frameLeft, text = "Selecciona un tipo de regimen:", font = ('Times', 12), background = '#fcfcfc', width = 25)
        lblRadicacionRegimen.grid(row = 6, column = 0, padx = 0, pady = (10, 2),  sticky = "ew")
        # ComboBox seleccionar el contrato con la EPS
        tipoRegimen = ttk.Combobox(frameLeft, values = self.__listadoRegimen, width = 30, font = ('Times', 10))
        tipoRegimen.current(0)
        tipoRegimen.grid(row = 7, column = 0, padx = 0, pady = 2,  sticky = "ew")
        tipoRegimen.bind("<<ComboboxSelected>>", setTipoSeleccion)
        
        # =========================================================================
        # | Frame Left Body
        # =========================================================================
        frameRight = tk.Frame(frame_form, bd=0, relief=tk.SOLID,bg='#fcfcfc',padx=30, pady=10)
        frameRight.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        
        # Label para ComboBox
        lblRadicacionRegimen = ttk.Label(frameRight, text = "Selecciona un segmento de ejecución:", font = ('Times', 12), background = '#fcfcfc', width = 25)
        lblRadicacionRegimen.grid(row = 0, column = 0, padx = 0, pady = (10, 2),  sticky = "ew")
        # ComboBox seleccionar el contrato con la EPS
        tipoSegmento = ttk.Combobox(frameRight, values = self.__listadoSegmentos, width = 30, font = ('Times', 10))
        tipoSegmento.current(0)
        tipoSegmento.grid(row = 1, column = 0, padx = 0, pady = 2,  sticky = "ew")
        tipoSegmento.bind("<<ComboboxSelected>>", setTipoSeleccion)

        # Label archivo de cuentas a procesar
        lblInfoProceso = ttk.Label(frameRight, text = "Información contrato y regimen.", font = ('Times', 12), background = '#fcfcfc')
        lblInfoProceso.grid(row = 2, column = 0, padx = 2, pady = 0, sticky = "w")
        
        # Cuadro de texto del archivo de cuentas a procesar
        txtInfoProceso = ttk.Entry(frameRight, width = 70)
        txtInfoProceso.grid(row = 3, column = 0, padx = 0, pady = (2, 10), sticky = "ew")
        txtInfoProceso.insert(0, "Proceso Sin Configurar")
        txtInfoProceso.configure(state = 'disabled')       
        
        # Label Fecha del radicado
        lblFechaProceso = ttk.Label(frameRight, text = "Fecha de configuración para RIPS [2023-03-15]", font = ('Times',  10), background = '#fcfcfc')
        lblFechaProceso.grid(row = 4, column = 0, padx = 2, pady = 0, sticky = "w")
        
        # Cuadro de texto de la fecha del radicado
        txtFechaProceso = ttk.Entry(frameRight, width=70)
        txtFechaProceso.grid(row=5, column=0, padx=0, pady=(2, 10), sticky="ew")
        txtFechaProceso.insert(0,"")
        
        # Label para el número de Radicado
        lblRelacionEnvio = ttk.Label(frameRight, text = "Escribe el número de relación de Envío en caso de ser necesario", font = ('Times', 10), background = '#fcfcfc')
        lblRelacionEnvio.grid(row = 6, column = 0, padx = 2, pady = 0, sticky = "w")
        
        # Cuadro de texto para el número del radicado
        txtRelacionEnvio = ttk.Entry(frameRight, width=70)
        txtRelacionEnvio.grid(row=7, column=0, padx=0, pady=(2, 15), sticky="ew")
        txtRelacionEnvio.insert(0,"")

        # Configuración adicional para agregar botones en la parte inferior.
        frameBtns = tk.Frame(frameRight, bd=0, relief=tk.SOLID,bg='#fcfcfc', padx=0, pady=5)
        frameBtns.grid(row=8, column=0, padx=0, pady=0,  sticky="ew")

        btnContratos = ttk.Button(frameBtns, text = "Validación y ejecución de proceso", style = "Accent.TButton", width = 70, command = Execute)
        btnContratos.grid(row = 9, column = 0, columnspan = 2, padx = 0, pady = 10)
        
        # Endregion - rightbody
        # Endregion  - Cuerpo principal del formulario 
        self.ventana.mainloop()

# Metodo para inicializar el metodo ventana principal    
if __name__ == '__main__':
    VentanaPrincipalForm()