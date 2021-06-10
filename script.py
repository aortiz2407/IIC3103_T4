""""
¡Bienvenido a mi script de descarga de datos!

Países escogidos:
    - Estados Unidos: USA
    - India: IND
    - Brasil: BRA
    - China: CHN
    - Argentina: ARG
    - Chile: CHL
"""""
# imports
import requests
import read_files
import gspread

URL = "http://tarea-4.2021-1.tallerdeintegracion.cl/gho_%s.xml"
codigo_paises = ["USA", "IND", "BRA", "CHN", "ARG", "CHL"]
urls_a_explorar = []
nombres_archivos_creados = []

print("¡¡BIENVENID@!!")
print("COMENZANDO A DESCARGAR ARCHIVOS DE DATOS --------------------------------------")

# Por cada país en la lista de países seleccionados, voy a pedir su archivo y voy a imprimir si esto se realiza bien
for pais in codigo_paises:
    print("Comenzando la descarga de ", pais, "  *************************")

    # Luego, voy a reemplazar el código del país en la URL original
    url_pais = URL % pais

    # Voy a agregar la url a las urls que estoy explorando y la imprimo
    urls_a_explorar.append(url_pais)
    print("La URL a utilizar es: ", url_pais)

    # Hago el request con la URL actual
    archivo_xml = requests.get(url_pais)

    # Chequeo si el código de estado de este archivo está funcionando
    print("Código de estado ", archivo_xml.status_code)  # debería imprimir 200 si está bien descargado y funciona

    # Creo el archivo en mi carpeta actual con el nombre correspondiente y lo guardo
    nombre_archivo_carpeta = "data_" + pais + ".xml"
    archivo_carpeta = open(nombre_archivo_carpeta, 'wb')
    archivo_carpeta.write(archivo_xml.content)
    archivo_carpeta.close()
    nombres_archivos_creados.append(nombre_archivo_carpeta)

print("FINALIZA LA DESCARGA DE ARCHIVOS DE DATOS -------------------------------------- /n /n")


# Linea a comentar si es que se descargan de nuevo los archivos
# nombres_archivos_creados = ["data_USA.xml", "data_IND.xml", "data_BRA.xml", "data_CHN.xml", "data_ARG.xml", "data_CHL.xml"]

print("COMIENZA EL FILTRO DE DATOS ---------------------------------------------------")
# Genero una lista gigante para guardar la data de todos los países en filas (que también son listas) -> lista de listas
all_filas = []

# Agrego la primera fila
primera_fila = ["GHO", "COUNTRY", "SEX", "YEAR", "GHECAUSES", "AGEGROUP", "Display", "Numeric", "Low", "High"]
all_filas.append(primera_fila)

# Por cada archivo (correspondiente a un país) voy a obtener los datos que quiero [más info en read_files]
for nombre_archivo_pais in nombres_archivos_creados:

    # Obtengo los datos filtrados
    data_filtrada = read_files.obtener_data(nombre_archivo_pais)

    # Voy a recorrer los datos filtrados
    for i in range(len(data_filtrada)):
        # Obtenemos la data a colocar
        data_a_poner = []

        # Por cada columna de la primera fila (obtengo los datos de cada columna de esta fila)
        for columna in primera_fila:
            data_a_poner.append(data_filtrada[i][columna])

        # Inserta una fila en la worksheet: le damos la data y la posición en que la vamos a colocar
        all_filas.append(data_a_poner)

# Reviso qué es lo que se está guardando
for elem in all_filas:
    print(elem)

# Imprimo la cantidad total de filas
print("FINALMENTE TENEMOS ", len(all_filas), " CANTIDAD DE DATOS")

print("TERMINA EL FILTRO DE DATOS ---------------------------------------------------")


print("COMIENZA ESCRITURA EN SHEETS -------------------------------------------------")

# Creamos la cuenta de servicio
gc = gspread.service_account(filename='credentials.json')

# Aquí vamos a abrir el archivo de sheets
sh = gc.open_by_key('1zUcAn-3kdUaQkQgYlGn9YE8rxacDgHceAv8_UDBUALk')
worksheet = sh.sheet1

# Insertamos todas las filas en el sheet
worksheet.insert_rows(all_filas)

print("TERMINA ESCRITURA EN SHEETS --------------------------------------------------")
