from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import pandas as pd

# 'time' is imported but not strictly needed; WebDriverWait is preferred

def main():
    service = Service(ChromeDriverManager().install())
    option =  webdriver.ChromeOptions()
    # option.add_argument("--headless")
    option.add_argument("--window-size=1920,1080")
    driver = Chrome(service=service, options=option)
    # 1. abrir el sitio de Mercado Libre para la búsqueda de laptops
    url = "https://listado.mercadolibre.com.mx/laptop"
    driver.get(url)

    # 2. esperar a que la lista de productos se cargue en la página
    try:
        wait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.ui-search-layout__item"))
        )
    except Exception as e:
        print("Advertencia: no se encontró el listado de productos dentro del tiempo límite.", e)

    # 3. obtener el HTML completo tras la carga
    html = driver.page_source

    # 4. analizar con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # 5. extraer los datos de cada producto
    productos = soup.select("li.ui-search-layout__item")

    # 5. extraer los datos de cada producto
    nombres = []
    precios = []
    enlaces = []

    for elemento in productos:
        # enlace del producto
        enlace_tag = elemento.find("a", class_="poly-component__title")
        enlace = enlace_tag["href"] if enlace_tag and enlace_tag.has_attr("href") else ""
        enlaces.append(enlace)

        # nombre/título
        titulo_tag = elemento.find("a", class_="poly-component__title")
        nombres.append(titulo_tag.get_text(strip=True) if titulo_tag else "")

        # precio: buscar en poly-price__current
        precio_div = elemento.find("div", class_="poly-price__current")
        if precio_div:
            precio_tag = precio_div.find("span", class_="andes-money-amount__fraction")
            precios.append(precio_tag.get_text(strip=True) if precio_tag else "")
        else:
            precios.append("")

    # 6. crear DataFrame con pandas
    df = pd.DataFrame({"Producto": nombres, "Precio": precios, "Link": enlaces})

    # 7. mostrar el DataFrame (puede ser vacío si no se encontraron productos)
    print(df)

    # 8. guardar en CSV
    df.to_csv("productos_mercadolibre.csv", index=False)

    # cerrar el navegador
    driver.quit()

 
if __name__ =="__main__":
    main()