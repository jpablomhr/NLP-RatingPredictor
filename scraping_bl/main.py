from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Seleccionamos el libro 'El hombre en busca del sentido' de buscalibre.
url = 'https://www.buscalibre.cl/libro-el-hombre-en-busca-de-sentido/9788425432026/p/47056974'

## Creamos el driver y configuramos el navegador según versiones.
service = Service(ChromeDriverManager().install())
option = webdriver.ChromeOptions()
driver = Chrome(service=service, options=option)
driver.get(url)

## Intentar cargar más reseñas con el botón de 'load comments'
try:
    load_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "load-comments"))
    )
    load_button.click()
    time.sleep(5)
except TimeoutException:
    print("The 'load comments' button has timed out.")
except NoSuchElementException:
    print("The 'load comment' button wasn't founded.")
except Exception as e:
    print('Unexpected error:', e)

# Creamos una lista que contendrá las reseñas y las estrellas.
reviews = []

try:
    # Utilizamos WebDriverWait para esperar a que todas las reseñas estén presentes.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[id^="texto-review-"]'))
    )

    # Extraemos todas las reseñas y los elementos de las estrellas.
    review_elements = driver.find_elements(By.CSS_SELECTOR, 'span[id^="texto-review-"]')
    star_elements = driver.find_elements(By.CSS_SELECTOR, 'span[class*="stars-"]')

    # Extraemos las reseñas y las estrellas, y las almacenamos en una lista 'reviews'.
    for review_element, star_element in zip(review_elements, star_elements):
        review_text = review_element.text.strip()
        star_class = star_element.get_attribute('class')  # Obtener la clase del elemento de estrellas

        # Extraer el número de estrellas de la clase
        star_rating = None
        for cls in star_class.split():
            if cls.startswith('stars-'):
                star_rating = cls.split('stars-')[-1]
                break

        # Validar que el número de estrellas esté en el rango correcto (1 a 5)
        if star_rating and star_rating.isdigit():
            star_rating = int(star_rating)
            if 1 <= star_rating <= 5:
                print('Reseña: ', review_text)
                print('Estrellas: ', star_rating)
                reviews.append({'Reseña': review_text, 'Estrellas': star_rating})

except Exception as e:
    print('Error when extracting reviews:', e)

# Dataframe de reseñas y estrellas.
df = pd.DataFrame(reviews, columns=["Reseña", "Estrellas"])
print(df.head())

df.to_csv('reseña.csv', index=False, encoding='utf-8')

driver.quit()












