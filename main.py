#import pagina1
#import pagina2
#import pagina3
#import pandas as pd

#def main():
#    print("Seleccione la página para realizar el web scraping:")
#    print("1. Página 1 (airbnb.mx)")
#    print("2. Página 2 (ROMS)")
#    print("3. Página 3 (MercadoLibre)")

#    opcion = input("Ingrese el número de la página: ")
#    formato = input("Ingrese el formato de salida ('tabla' o 'lista'): ")

#    if opcion == '1':
#        datos = pagina1.scrape_pagina1(formato)
#    elif opcion == '2':
#        datos = pagina2.scrape_pagina2(formato)
#    elif opcion == '3':
#        datos = pagina3.scrape_pagina3(formato)
#    else:
#        print("Opción no válida")
#       return

    # Guardar los datos en un archivo CSV

#    if isinstance(datos, pd.DataFrame):
#        datos.to_csv('datos_scraping.csv', index=False)
#    elif isinstance(datos, list):
#        df = pd.DataFrame(datos)
#        df.to_csv('datos_scraping.csv', index=False)
#    else:
#        print("Error: Formato de datos no soportado")

#    print("Datos guardados en 'datos_scraping.csv'")

#if __name__ == "__main__":
#    main()

import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebAction:
    def __init__(self, driver, action):
        self.driver = driver
        self.action = action

    def execute(self):
        raise NotImplementedError("Execute method must be implemented by subclasses")

    def find_element(self, selector):
        print(f"Trying to find element with selector: {selector}")
        wait = WebDriverWait(self.driver, 10)
        
        try:
            if "id" in selector and selector["id"]:
                return wait.until(EC.presence_of_element_located((By.ID, selector["id"])))
        except NoSuchElementException:
            print(f"No element found with ID: {selector.get('id')}")

        try:
            if "class" in selector and selector["class"]:
                return wait.until(EC.presence_of_element_located((By.CLASS_NAME, selector["class"])))
        except NoSuchElementException:
            print(f"No element found with CLASS: {selector.get('class')}")

        try:
            if "placeholder" in selector and selector["placeholder"]:
                return wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@placeholder='{selector['placeholder']}']")))
        except NoSuchElementException:
            print(f"No element found with PLACEHOLDER: {selector.get('placeholder')}")

        try:
            if "aria-label" in selector and selector["aria-label"]:
                return wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@aria-label='{selector['aria-label']}']")))
        except NoSuchElementException:
            print(f"No element found with ARIA-LABEL: {selector.get('aria-label')}")

        try:
            if "name" in selector and selector["name"]:
                return wait.until(EC.presence_of_element_located((By.NAME, selector["name"])))
        except NoSuchElementException:
            print(f"No element found with NAME: {selector.get('name')}")

        raise NoSuchElementException("No valid selector found or element not found using provided selectors")

class ClickAction(WebAction):
    def execute(self):
        element = self.find_element(self.action["selector"])
        element.click()

class InputAction(WebAction):
    def execute(self):
        element = self.find_element(self.action["selector"])
        element.send_keys(self.action["value"])

class ExtractAction(WebAction):
    def execute(self):
        element = self.find_element(self.action["selector"])
        attribute = self.action.get("attribute", "text")
        if attribute == "text":
            return element.text
        else:
            return element.get_attribute(attribute)

class SubmitFormAction(WebAction):
    def execute(self):
        form = self.find_element(self.action["selector"])
        form.submit()

class WebAutomator:
    ACTION_CLASSES = {
        "click": ClickAction,
        "input": InputAction,
        "extract": ExtractAction,
        "submit_form": SubmitFormAction
    }

    def __init__(self, driver, url):
        self.url = url
        self.driver = driver
        self.actions = []

    def add_action(self, action_type, selector, value=None, attribute=None):
        action = {
            "type": action_type,
            "selector": selector
        }
        if value:
            action["value"] = value
        if attribute:
            action["attribute"] = attribute
        self.actions.append(action)

    def run(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        for action in self.actions:
            action_class = self.ACTION_CLASSES.get(action["type"])
            if action_class:
                action_instance = action_class(self.driver, action)
                try:
                    result = action_instance.execute()
                    if result:
                        print(f"Extracted data: {result}")
                except NoSuchElementException as e:
                    print(f"Error executing action {action['type']}: {str(e)}")
            else:
                print(f"Action {action['type']} not recognized")

        input("Press Enter to close the browser...")
        self.driver.quit()

def main():
    driver = webdriver.Chrome()
    automator = WebAutomator(driver, input("Enter the URL: "))

    while True:
        action_type = input("Enter action type (click, input, extract, submit_form) or 'exit' to stop: ").strip().lower()
        if action_type == 'exit':
            break

        selector = {
            "id": input("Enter ID (leave blank if not applicable): ").strip(),
            "class": input("Enter class (leave blank if not applicable): ").strip(),
            "placeholder": input("Enter placeholder (leave blank if not applicable): ").strip(),
            "aria-label": input("Enter aria-label (leave blank if not applicable): ").strip(),
            "name": input("Enter name (leave blank if not applicable): ").strip()
        }

        value = None
        attribute = None

        if action_type == "input":
            value = input("Enter the value to input: ").strip()
        elif action_type == "extract":
            attribute = input("Enter attribute to extract (default is 'text'): ").strip() or "text"

        automator.add_action(action_type, selector, value, attribute)

    automator.run()

if __name__ == "__main__":
    main()
