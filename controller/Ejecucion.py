# ===========================================================================
# Importaciones de clases y librerias necesarias en esta vista
# ===========================================================================
# Region - Importación de librerias y clases.
import requests
from psycopg2 import connect
from datetime import datetime, timedelta
from controller.utils.Helpers import Helpers
# Endregion - Importación de librerias y clases.

# Region - Inicialización de clases para uso de metodos.
helper = Helpers()
KEYENCRYPT = "B/eLEWVKODvmGPjhEltVcZEZZ6as9PeFfOcscyM="
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
        
        
        self.dataRadicarFecha = ""
        self.dataRadicarNumero = ""
        self.dataRadicarEPS = ""
        self.dataRadicarDaFram = ""

        # Variables relacionadas al lanzamiento del WorkFlow desde la API de ElectroNeek
        self.__keyNeekApi = helper.desEncriptarData(helper.getValue("APINeek", "key"))
        self.__urlNeekApi = helper.getValue("APINeek", "workFlowURL")
        self.__idNeekApi = helper.getValue("APINeek", "idWorkFlow")

        # Datos de conexión para la base de datos
        self.__hostDatabase = helper.desEncriptarData(helper.getValue("DataConex", "host"))
        self.__nameDatabase = helper.desEncriptarData(helper.getValue("DataConex", "dabd"))
        self.__userDatabase = helper.desEncriptarData(helper.getValue("DataConex", "user"))
        self.__passDatabase = helper.desEncriptarData(helper.getValue("DataConex", "pass"))
        self.__conn = ""
    
    def crearConexion(self):
        """
        Este metodo se encargará de gestionar la
        conexión a la base de datos de PgSQL, retornando
        la instancia de conexión para ser usada en otros lugares.
        """
        try:
            self.__conn = connect(
                    database = self.__nameDatabase, 
                    user = self.__userDatabase, 
                    host= self.__hostDatabase,
                    password = self.__passDatabase,
                    port = 5432
                )
        except Exception as e:
            self.__conn = ""
    
    def cerrarConexion(self):
        """
        Cada que se use la conexión a base de datos nueva,
        se deberá cerrar la misma para evitar procesos abiertos.
        """
        try:
            if(self.__conn != ""):
                self.__conn.close()
        except Exception as e:
            self.__conn = ""

    def cargarDataBaseDatos(self):
        """
        Este metodo se encargará de leer la información
        y cargar la misma a base de datos, según los parametros
        de configuración dados.
        """
        fechaEnvio = (datetime.today() - timedelta(hours = 0)).strftime('%Y-%m-%d %H:%M:%S')
        exito = False
        self.crearConexion()
        if(self.__conn != ""):
            try:
                cur = self.__conn.cursor() # Instancia del cursor para querys de DB
                # Query de inserción de datos.
                cur.execute(f"INSERT INTO data_armado(fechaRadicadoArmar, numeroRadicadoArmar , nombreEPSArmar, datosCuentasArmar, fechaPeticion)\
                         VALUES('{self.dataRadicarFecha}', '{self.dataRadicarFecha}', '{self.dataRadicarEPS}' {self.dataRadicarDaFram}, {fechaEnvio})");
                self.__conn.commit() # Commit de la query dada
                cur.close() # Cierre del cursor
                exito = True
            except Exception as e:
                exito = False
            finally:
                self.cerrarConexion() # Cierre de la conexión
                return exito

    def lanzarEjecucionBot(self):
        """
        Este metodo consumirá la API de ElectroNeek con el
        fin de ejecutar de manera remota el bot para armado
        de cuenta hosteado en una RDP.
        ? URL doc API: https://docs.electroneek.com/reference/postworkflow
        TODO: ID del WorkFlow de ElectroNeek.
        """
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.__keyNeekApi}"
        }

        response = requests.post(self.__urlNeekApi.replace("id", self.__idNeekApi), headers=headers)

        print(response.text)
    
    def orquestarEjecucion(self):
        """
        Este metodo se encargará de gestionar la ejecución de los datos.
        """
        return True
