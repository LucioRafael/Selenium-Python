from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

def scrape_pagina3(formato='tabla'):
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

    # Navegar a la página web
    driver.get('https://www.mercadolibre.com/')

    # Esperar unos segundos para que la página cargue completamente
    driver.implicitly_wait(10)

    # Extraer la información (por ejemplo, los productos destacados)
    productos = driver.find_elements(By.CSS_SELECTOR, '.promotion-item .promotion-item__title')

    datos = [producto.text for producto in productos]

    # Cerrar el navegador
    driver.quit()

    # Formatear los datos
    if formato == 'tabla':
        return pd.DataFrame(datos, columns=['Producto'])
    elif formato == 'lista':
        return datos
    else:
        raise ValueError("Formato no soportado: elija 'tabla' o 'lista'")
