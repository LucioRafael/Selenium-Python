from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Ruta al WebDriver de Edge
edge_driver_path = r'C:\Archivos\driverEdge\msedgedriver.exe'

# Configurar el servicio para Edge
service = Service(edge_driver_path)

# Configurar las opciones del navegador
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Iniciar el navegador Edge con las opciones configuradas
driver = webdriver.Edge(service=service, options=options)

# Navegar a la página web de clima
driver.get('https://www.clima.com/mexico/estado-de-coahuila-de-zaragoza/torreon')

# Esperar unos segundos para que la página cargue completamente
time.sleep(5)

# Extraer la información de clima
# Encuentra la tabla de clima (ajusta el selector según la estructura de la página)
tabla_clima = driver.find_element(By.CLASS_NAME, 'table')  # Actualiza este selector según sea necesario

# Extraer el encabezado de la tabla
encabezados = tabla_clima.find_elements(By.TAG_NAME, 'th')
encabezados_texto = [encabezado.text for encabezado in encabezados]

# Extraer todas las filas de la tabla
filas = tabla_clima.find_elements(By.TAG_NAME, 'tr')

# Crear una lista para almacenar los datos
datos_clima = []

# Recorrer las filas y extraer los datos
for fila in filas:
    encabezados = tabla_clima.find_elements(By.TAG_NAME, 'th')
    columnas = fila.find_elements(By.TAG_NAME, 'td')
    datos_fila = [columna.text for columna in columnas]
    datos_clima.append(datos_fila)

# Crear un DataFrame de pandas con los datos extraídos
df = pd.DataFrame(datos_clima)

# Guardar el DataFrame en un archivo de Excel
df.to_csv('clima_torreon.csv', index=False)

# Cerrar el navegador
driver.quit()

print("Datos de clima guardados en clima_torreon.xlsx")
