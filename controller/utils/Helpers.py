# region importando librerias necesarias
import os
import json
import shutil
import zipfile
import pathlib
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
# endregion importando librerias necesarias

# region Instanciar Objetos y variables Globales
relativePath = os.getcwd()
KEYENCRYPT = "ecTNu1JkrN8WOEZQ667dOGOqBcS9Peh0RShN83l1WK0="
f = Fernet(KEYENCRYPT)
# endregion importando librerias necesarias

# region Creando una clase
class Helpers:
    # Contructores e inicializadores
    def __init__(self):
        self.__routeConfig = relativePath + "/config.json"
        self.__initial_count = 0
    
    # region Metodos
    # Nos ayuda para traer las rutas completas del config
    def getRoutes(self, key, value):
        with open(self.__routeConfig, 'r') as file: 
            config = json.load(file)
            if config[key][value] == "":
                file.close()
            else:
                route = str(config[key][value])
                file.close()
        
        fullpath = relativePath + route
        return fullpath
    
    def encriptarData(self, valor: str):
        """
            Se encrypta un dato dado, en tipo str para
            hacer su encryptación a través de la llave
            recibida en el llamado del metodo
        - `Args:`
            - valor (str): Valor del metodo a encryptar
        - `Returns:`
            - str: Valor encryptado
        """
        token = f.encrypt(str.encode(valor)).decode("utf-8")
        return token
        
    def desEncriptarData(self, valor: str):
        """
            Toma la llave de encriptación, y el
            valor a desencriptar, y retorna el valor
            en formato str.
            - `Args:`
                - valor (str): Valor a desencriptar
            - `Returns:`
                - texto (str): Valor desencriptado en UTF8
        """
        texto = f.decrypt(valor)
        return texto.decode("utf-8")

    # Nos ayuda a extraer un valor del config
    def getValue(self, key, value):
        with open(self.__routeConfig, 'r') as file: 
            config = json.load(file)
            if config[key][value] == "":
                file.close()
            else:
                data = str(config[key][value])
                file.close()
        
        return data
    
    # Nos permite cargar una imagen de forma dinamica
    def getImage(self, key, size):
        # Abrir la imagen
        image = Image.open(self.getRoutes(key, "Value"))
        # Redimensionar la imagen con el filtro LANCZOS (anteriormente ANTIALIAS)
        image = image.resize(size, Image.Resampling.LANCZOS)
        # Convertir a un objeto PhotoImage de Tkinter
        return ImageTk.PhotoImage(image)  

    #Nos permite realizar un centrado de la ventana
    def centerWindows(self,windows,height,withs):    
        pantall_ancho = windows.winfo_screenwidth()
        pantall_largo = windows.winfo_screenheight()
        x = int((pantall_ancho/2) - (withs/2))
        y = int((pantall_largo/2) - (height/2))
        return windows.geometry(f"{withs}x{height}+{x}+{y}")
    
    # Nos permite habilitar ingresar valor y deshabilitar
    def SetInfoDisabled(self, inputTxt, value):
        inputTxt.configure(state='normal')
        inputTxt.delete(0,"end")
        inputTxt.insert(0,str(value))
        inputTxt.configure(state='disabled')
    
    # Nos permite contar los valorer de los data frame sin las columnas
    def countData(self,totalcount):
        aloneRows = totalcount.split(",")
        total = str(aloneRows[0]).replace("(", "")
        return total
    
    # Nos permite realizar el conteo de las carpetas
    def countFolder(self,ruta):
        self.__initial_count = 0
        for path in pathlib.Path(ruta).iterdir():
            if path.is_dir():
                self.__initial_count += 1
                
        return self.__initial_count
    
    # Metodo para extraer un archivo zip sin duplicarse
    def extractZip(self,rutaZip):
        rutaConfig = rutaZip.split('\\')
        deleteFile = rutaConfig[-1]
        deleteZip = deleteFile.replace(".zip","")
        ruta_extraccion = rutaZip.replace(deleteFile,"")
        ruta_extraida = ruta_extraccion + "\\" + deleteZip
        #print(ruta_extraccion + "\\" + deleteZip)
        
        try:
            shutil.rmtree(ruta_extraida)
        except OSError as e:
            print("No hay ruta para eliminar " + str(e))
            
        archivo_zip = zipfile.ZipFile(rutaZip, "r")
        try:
            archivo_zip.extractall(path=ruta_extraccion)
        except Exception  as e:
            print(str(e))
        archivo_zip.close()
        return ruta_extraida
    
    # Metodo para realizar la validacion del destino
    def ValidateDestiny(self, ruta):
        cont = 0
        dir = ruta
        for f in os.listdir(dir):
            cont += 1
        return cont
    # endregion Metodos
# endregion