# ===========================================================================
# Importaciones de clases y librerias necesarias en esta vista
# ===========================================================================
# Region - Importación de librerias y clases.
from controller.Peticiones import Peticiones
from controller.utils.Helpers import Helpers
from datetime import datetime
# Endregion - Importación de librerias y clases.

# Region - Inicialización de clases para uso de metodos.
helper = Helpers()
peti = Peticiones()
# Endregion - Inicialización de clases para uso de metodos.

# Clase pivote para realizar la ejecución del bot. 
class Ejecucion:
    """
    Esta clase se encargará de enviar la información
    recolectada por el formulario a la base de datos
    de PgSQL, de manera que el bot de armado solo deba
    consultar la tabla asignada.
    """
    # Contructores e inicializadores de clase
    def __init__(self):
        """
        Constructor de la clase, se inicializarán las
        variables a utilizar dentro de la base de datos
        y se re asignaran sus valores luego de que se
        complete el formulario.
        """
        self.formIPS = ""
        self.formEPS = ""
        self.formContrato = ""
        self.formRegimen = ""
        self.formSegmento = ""
        self.formEstado = ""
        self.formFecha = ""
        self.formValidacion = ""

        self.__botEjecutar = ""

    def _definirMongoDataAPI(self):
        """
        Este metodo se encargará de setear la data para
        ser enviada a la API de Radicación de Zentria y
        así poder ser consultada por otros bots.
        """
        if not self.formFecha:
            self.formFecha = datetime.now().strftime("%Y/%m/%d")
        dictDatosFormulario = {
            "ips": self.formIPS,
            "eps": self.formEPS,
            "contrato": self.formContrato,
            "regimen": self.formRegimen,
            "estado": self.formEstado,
            "segmento": self.formSegmento,
            "fecha": self.formFecha,
            "numero_relacion_envio": self.formValidacion
        }
        return dictDatosFormulario            
        
    
    def _definirPostgresDataAPI(self):
        """
        Este metodo se encargará de setear la data para
        ser enviada a la API de Radicación de Zentria y
        así poder ser consultada por otros bots.
        """
        if not self.formFecha:
            self.formFecha = datetime.now().strftime("%Y/%m/%d")
        objetoDato={
                "numero_radicado": self.formValidacion,
                "fecha_rips": "",
                "fecha_soporte": "",
                "fecha_eapb": ""
        }            
        if("2" in self.formSegmento):
            # El 2 no ejecuta bot
            #self.__botEjecutar = "idWorkFlowCargarSoportesSFTP"
            objetoDato["fecha_rips"] = self.formFecha
            return objetoDato, "certificado-rips"
        if("3" in self.formSegmento):
            #self.__botEjecutar = "idWorkFlowCargarSoportesSFTP"
            objetoDato["fecha_soporte"] = self.formFecha
            return objetoDato, "soportes-eapb"
        if("4" in self.formSegmento):
            #self.__botEjecutar = "idWorkFlowCargarSoportesSFTP"
            objetoDato["fecha_eapb"] = self.formFecha
            return objetoDato, "radicado-eapb"
        

    def orquestarEjecucion(self):
        """
        Este metodo se encargará de validar el tipo de proceso
        que se estará ejecutando, y según el mismo, ejecutar
        la API de ElectroNeek para la ejecución de los bots.
        """
        exito = { "status": False, "mensaje": "" }
        try:
            if("1" in self.formSegmento):
                self.__botEjecutar = "idWorkFlowGeneracionRIPS"
                peti.ejecutarBotElectroNeek(self.__botEjecutar)
                datos = self._definirMongoDataAPI()
                peti.subirDatosFormulario(datos)
                return
            if("2" not in self.formSegmento):
                peti.ejecutarBotElectroNeek(self.__botEjecutar)
            datos, segmento = self._definirPostgresDataAPI()
            peti.actualizarFechaRelacionEnvio(datos, segmento)
        except Exception as e:
            exito["mensaje"] = f"Ocurrió un error en la ejecución del formulario, error: {e}"
        finally:
            return exito
