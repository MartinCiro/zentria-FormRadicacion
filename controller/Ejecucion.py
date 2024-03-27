# ===========================================================================
# Importaciones de clases y librerias necesarias en esta vista
# ===========================================================================
# Region - Importación de librerias y clases.
from controller.Peticiones import Peticiones
from controller.utils.Helpers import Helpers
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
        self.formCotnrato = ""
        self.formRegimen = ""
        self.formSegmento = ""
        self.formFecha = ""
        self.formValidacion = ""

        self.__botEjecutar = ""

    def _definirDataAPI(self):
        """
        Este metodo se encargará de setear la data para
        ser enviada a la API de Radicación de Zentria y
        así poder ser consultada por otros bots.
        """
        dictDatosFormulario = {
            "ips": self.formIPS,
            "eps": self.formEPS,
            "contrato": self.formCotnrato,
            "regimen": self.formRegimen,
            "segmento": self.formSegmento,
            "fecha": self.formFecha,
            "numero_relacion_envio": self.formValidacion
        }
        if("1" in self.formSegmento):
            self.__botEjecutar = "idWorkFlowGeneracionRIPS"
        if("2" in self.formSegmento):
            self.__botEjecutar = "idWorkFlowCargarSoportesSFTP"
        if("2" in self.formSegmento):
            self.__botEjecutar = "idWorkFlowCargarSoportesSFTP"
        return dictDatosFormulario
    
    def orquestarEjecucion(self):
        """
        Este metodo se encargará de validar el tipo de proceso
        que se estará ejecutando, y según el mismo, ejecutar
        la API de ElectroNeek para la ejecución de los bots.
        """
        exito = { "status": False, "mensaje": "" }
        try:
            datos = self._definirDataAPI()
            peti.subirDatosFormulario(datos)
            if("3" not in self.formSegmento):
                peti.ejecutarBotElectroNeek(self.__botEjecutar)
            else:
                peti.actualizarFechaRelacionEnvio(datos["numero_relacion_envio"], datos["fecha"], "RADICADO ENTIDAD")
        except Exception as e:
            exito["mensaje"] = f"Ocurrió un error en la ejecución del formulario, error: {e}"
        finally:
            return exito
