### RenombreZentriaForm

Aplicativo de formulario, encargado de recopilar la data necesaria para la ejecución del bot de armado de cuentas y renombre del proyecto Zentria.

## Parametros para ejecución

Este formulario toma datos traídos desde el endpoint ***http://172.206.196.43:3200/consultarSedes*** de manera que podrá obtener la información de:

* EPS registradas
* IPS registradas

* Contratos

De esa manera podremos pintar los datos en el formulario, para luego ser envíados al endpoint ***http://172.206.196.43:3100Mongo/datosFormulario*** y de esa manera cargar la información de la solicitud según el segmento deseado.
