import requests as rq
from json import loads
# from controller.Log import Log
from controller.utils.Helpers import Helpers
# from controller.utils.Configurations import Configurations

# logger = Log()
helper = Helpers()
# config = Configurations()

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

        self.__urlAPI = helper.getValue("Variables", "URLApi")
        self.__urlAPIRadicacion = helper.getValue("Variables", "URLApi")
        self.__dictEndpoints = {
            "obtencionFacturasArmado": "postgres/itemsActividadesConArmado",
            "actualizacionEstadoRadicacion": "postgres/EstadoRadicado",
            "consultarSedes": "postgres/consultarSedes"
        }
    
    def obtenerSedes(self):
        """
        Metodo encargado de la consulta de sedes actuales
        del proyecto de Zentria.
        """
        response = []
        try:
            res = rq.get(f"{self.__urlAPI}/{self.__dictEndpoints["consultarSedes"]}")
            response = loads(res.text)
        except Exception as e:
            print(f"Error al generar la petición para la consulta de sedes, error: {e}")
        finally:
            return response

    # def obtenerListadoFacturas(self):
    #     """
    #     Este metodo hará una petición a la API para obtener el
    #     listado de facturas que se pueden armar su cuenta.
    #     """
    #     respuesta = []
    #     try:
    #         respuesta = loads(res.text)
    #     except Exception as e:
    #         print(f"Error al generar la petición de facturas para armado de cuentas, error: {e}")
    #     finally:
    #         return respuesta
    
    def actualizarEstadoCuenta(self, idFactura: int, estado: str):
        """
        Actualización del estado de la factura en la tabla de items_facturas
        a su nuevo estado, según culminación de proceso x factura.
        - `Args:`
            - idFactura (int): Id de la factura en la tabla.
            - estado (str): Estado que se le asignará.
        """
        exito = False
        try:
            data = {
                "id_pdf_factura": idFactura,
                "estado_proceso": estado
            }
            actualizacion = rq.post(
                f"{self.__urlAPI}/{self.__dictEndpoints["actualizacionEstado"]}",
                json = data
            )
            print(actualizacion.text)
        except Exception as e:
            print(f"No se ha podido actualizar los datos de la cuenta con id: {idFactura}, error: {e}")
        finally:
            return exito