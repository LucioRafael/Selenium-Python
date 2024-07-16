from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd

def scrape_pagina1(formato='tabla'):
    # Configurar las opciones del navegador
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/113.0.0.0 Safari/537.36")
    # opts.add_argument("--headless")  # Descomentar si deseas ejecutar en modo headless

    # Iniciar el navegador Edge con las opciones configuradas
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=opts)

    # Navegar a la página web
    driver.get('https://www.airbnb.com/')

    # Esperar unos segundos para que la página cargue completamente
    sleep(3)

    # Extraer los títulos de los anuncios
    titulos_anuncios = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')
    datos = [{'Título': titulo.text} for titulo in titulos_anuncios]

    # Cerrar el navegador
    driver.quit()

    # Formatear los datos
    if formato == 'tabla':
        df = pd.DataFrame(datos)
        df.index.name = 'N°'
        df.reset_index(inplace=True)
        return df
    elif formato == 'lista':
        return datos
    else:
        raise ValueError("Formato no soportado: elija 'tabla' o 'lista'")

# Ejemplo de uso
if __name__ == "__main__":
    resultado = scrape_pagina1('tabla')
    print(resultado)
