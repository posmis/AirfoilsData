import requests
from bs4 import BeautifulSoup


def get_airfoil_names():
    url = "http://airfoiltools.com/search/airfoils"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Проверка на ошибки

        soup = BeautifulSoup(response.text, "html.parser")

        airfoil_links = soup.find_all("a", href=True)
        airfoil_names = []
        for link in airfoil_links:
            href = link["href"]
            if "/airfoil/details?airfoil=" in href:
                name = href.split("=")[1]
                airfoil_names.append(name)
        airfoil_names = list(set(airfoil_names))
        airfoil_names.sort()

        return airfoil_names

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к сайту: {e}")
        return []


def save_airfoil_names_to_file(airfoil_names, file_path):
    with open(file_path, "w") as file:
        for name in airfoil_names:
            file.write(name + "\n")
    print(f"Названия профилей сохранены в файл: {file_path}")

airfoil_names = get_airfoil_names()
if airfoil_names:
    save_airfoil_names_to_file(airfoil_names, "../data/airfoil_names.txt")
else:
    print("Не удалось получить названия профилей.")