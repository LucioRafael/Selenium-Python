from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd

def scrape_pagina2(formato='tabla'):
    # Configurar las opciones del navegador
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/113.0.0.0 Safari/537.36")
    # opts.add_argument("--headless")  # Descomentar si deseas ejecutar en modo headless

    # Iniciar el navegador Edge con las opciones configuradas
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=opts)

    # Navegar a la página web
    driver.get('https://www.retrostic.com/es/roms')

    # Esperar unos segundos para que la página cargue completamente
    sleep(3)

    # Extraer la tabla de juegos
    tabla_juegos = driver.find_element(By.CLASS_NAME, 'table-hover')
    filas = tabla_juegos.find_elements(By.TAG_NAME, 'tr')
    
    # Extraer encabezados
    encabezados = [th.text for th in filas[0].find_elements(By.TAG_NAME, 'th')]

    # Extraer filas de datos
    datos = []
    imagen_counter = 1
    for fila in filas[1:]:
        columnas = fila.find_elements(By.TAG_NAME, 'td')
        fila_datos = [columna.text for columna in columnas]
        # Si hay una columna de imagen vacía, agregar "Imagen X"
        if len(fila_datos) < len(encabezados):
            fila_datos.append(f'Imagen {imagen_counter}')
            imagen_counter += 1
        datos.append(fila_datos)

    # Cerrar el navegador
    driver.quit()

    # Formatear los datos
    if formato == 'tabla':
        df = pd.DataFrame(datos, columns=encabezados)
        return df
    elif formato == 'lista':
        return datos
    else:
        raise ValueError("Formato no soportado: elija 'tabla' o 'lista'")

# Ejemplo de uso
if __name__ == "__main__":
    resultado = scrape_pagina2('tabla')
    print(resultado)
