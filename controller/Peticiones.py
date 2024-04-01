import requests as rq
from json import loads, dumps
from controller.utils.Helpers import Helpers

helper = Helpers()

class Peticiones:
    """
    Peticiones
    ==========
    Esta clase se encargará de realizar las peticiones
    correspondientes a la API de Zentria, de manera
    que pueda obtener la info con la que trabajará el
    armado de cuenta, y a la vez, reportar información
    del mismo armado.
    - `Metodos disponibles:`
        - `obtenerListadoFacturas` -> Dict: Obtención de cuentas para armado.
    """

    def __init__(self) -> None:
        """Contructor de la clase"""
        # Variables relacionadas al lanzamiento del WorkFlow desde la API de ElectroNeek
        self.__keyNeekApi = helper.desEncriptarData(helper.getValue("APINeek", "key"))
        self.__urlNeekApi = helper.getValue("APINeek", "workFlowURL")

        self.__urlAPI = helper.getValue("Variables", "URLApi")
        self.__urlAPIRadicacion = helper.getValue("Variables", "URLApiRadicacion")
        self.__dictEndpoints = {
            "consultarSedes": "postgres/consultarSedes",
            "subirFormulario": "mongo/datosFormulario"
        }
    
    def obtenerSedes(self):
        """
        Metodo encargado de la consulta de sedes actuales
        del proyecto de Zentria.
        """
        response = []
        try:
            res = rq.get(f"{self.__urlAPI}/{self.__dictEndpoints["consultarSedes"]}", timeout = 10)
            response = loads(res.text)
        except Exception as e:
            print(f"Error al generar la petición para la consulta de sedes, error: {e}")
        finally:
            return response

    def subirDatosFormulario(self, datosFormulario: dict):
        """
        Este metodo se encargará de enviar los datos a la base de
        datos de MongoDB, mediante un endpoint de la API de Zentria.
        """
        respuesta = []
        try:
            print(f"\t - URL: {self.__urlAPIRadicacion}/{self.__dictEndpoints["subirFormulario"]}")
            res = rq.post(
                url = f"{self.__urlAPIRadicacion}/{self.__dictEndpoints["subirFormulario"]}",
                json = datosFormulario,
                timeout = 10
            )
            respuesta = loads(res.text)
            print(f"\n Respuesta de la carga de info al formulario: \n - {respuesta}")
        except Exception as e:
            print(f"Falló en la carga de datos del formulario, error: {e}")
        finally:
            return respuesta
    
    def ejecutarBotElectroNeek(self, idBot: str):
        """
        Actualización del estado de la factura en la tabla de items_facturas
        a su nuevo estado, según culminación de proceso x factura.
        - `Args:`
            - idBotElectroNeek (str): Llave identificadora del bot de ElectroNeek.
        """
        exito = False
        try:
            idBotElectroNeek = helper.getValue("APINeek", idBot)
            self.__urlNeekApi = self.__urlNeekApi.replace("$id$", idBotElectroNeek)
            cabeceras = { "accept": "application/json", "content-type": "application/json", "authorization": f"Bearer {self.__keyNeekApi}" }
            ejecutarBot = rq.post(url = self.__urlNeekApi, headers = cabeceras)
            print(dumps(ejecutarBot.text, indent = 4))
            exito = True
        except Exception as e:
            print(f"Imposible ejecutar el lanzamiento del bot en ElectroNeek API, error: {e}")
        finally:
            return exito
    
    def actualizarFechaRelacionEnvio(self, relacionEnvio: str, fecha: str, estado: str):
        """
        Este metodo actualizará la fecha y el estado de una relación
        de envío dada, mediante un endpoint.
        `Args:`
            `relacionEnvio (str):` Número de la relación de envío
            `fecha (str):` Fecha a actualizar en campo (Fecha Radicado || Fecha relación envío)
            `estado (str):` Estado para actualizar en la relación de envío
        """
        # ! TODO
