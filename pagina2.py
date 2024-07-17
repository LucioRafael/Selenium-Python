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

    try:
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
        for fila in filas[1:]:
            columnas = fila.find_elements(By.TAG_NAME, 'td')
            fila_datos = [columna.text for columna in columnas]
            datos.append(fila_datos)

        # Depuración: imprimir filas y datos extraídos
        print("Encabezados:", encabezados)
        for dato in datos:
            print("Fila de datos:", dato)

    except Exception as e:
        print("Error durante el scraping:", e)
    finally:
        # Cerrar el navegador
        driver.quit()

    # Formatear los datos
    if formato == 'tabla':
        df = pd.DataFrame(datos, columns=encabezados)
        return df
    elif formato == 'lista':
        # Filtrar los nombres de los juegos y agregar la enumeración
        lista_datos = []
        for i, fila_datos in enumerate(datos, start=1):
            nombre = fila_datos[1] if len(fila_datos) > 1 else "N/A"  # El campo "Nombre" es el segundo en la fila
            lista_datos.append({'Número': i, 'Nombre': nombre})
        return lista_datos
    else:
        raise ValueError("Formato no soportado: elija 'tabla' o 'lista'")

# Ejemplo de uso
if __name__ == "__main__":
    resultado = scrape_pagina2('lista')
    for item in resultado:
        print(item)
