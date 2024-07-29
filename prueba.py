import requests
from bs4 import BeautifulSoup

# URL del menú
url = "https://www.firecapitano.com/menus"

# Hacer una solicitud GET a la página web
response = requests.get(url)

# Crear un objeto BeautifulSoup con el contenido HTML de la página
soup = BeautifulSoup(response.content, 'html.parser')


# Encontrar las secciones del menú (ajusta las clases según la estructura HTML real)
menu_sections = soup.find_all('div', class_='menu-section')
print(menu_sections)
# Recorrer cada sección y extraer los elementos de los platos y sus precios
for section in menu_sections:
    print(section)
    section_title = section.find('h2').get_text(strip=True)
    print(f"Sección: {section_title}")
    
    items = section.find_all('div', class_='menu-item')
    for item in items:
        item_name = item.find('h3').get_text(strip=True)
        item_price = item.find('span', class_='price').get_text(strip=True)
        print(f"{item_name}: {item_price}")

    print("\n")

# Nota: Asegúrate de verificar y ajustar las clases y etiquetas según la estructura HTML específica de la página
