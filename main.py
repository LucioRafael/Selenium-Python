import pagina1
import pagina2
import pagina3
import pandas as pd

def main():
    print("Seleccione la página para realizar el web scraping:")
    print("1. Página 1 ()")
    print("2. Página 2 (ROMS)")
    print("3. Página 3 (MercadoLibre)")

    opcion = input("Ingrese el número de la página: ")
    formato = input("Ingrese el formato de salida ('tabla' o 'lista'): ")

    if opcion == '1':
        datos = pagina1.scrape_pagina1(formato)
    elif opcion == '2':
        datos = pagina2.scrape_pagina2(formato)
    elif opcion == '3':
        datos = pagina3.scrape_pagina3(formato)
    else:
        print("Opción no válida")
        return

    # Guardar los datos en un archivo CSV
    if isinstance(datos, pd.DataFrame):
        datos.to_csv('datos_scraping.csv', index=False)
    elif isinstance(datos, list):
        df = pd.DataFrame(datos)
        df.to_csv('datos_scraping.csv', index=False)
    else:
        print("Error: Formato de datos no soportado")

    print("Datos guardados en 'datos_scraping.csv'")

if __name__ == "__main__":
    main()
