from typing import List
import requests
import os

def download_data(airfoil_name: str, reynolds: List[int]):
    airfoil_url = f"http://airfoiltools.com/airfoil/lednicerdatfile?airfoil={airfoil_name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    save_folder = os.path.join("../data", airfoil_name)
    os.makedirs(save_folder, exist_ok=True)
    aifoil_file = os.path.join(save_folder, f"{airfoil_name}_airfoil.dat")

    try:
        response = requests.get(airfoil_url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(aifoil_file, 'w') as file:
                file.write(response.text)
            print(f"Данные профиля {airfoil_name} сохранены в {aifoil_file}")
        else:
            print(f"Ошибка: Не удалось скачать данные профиля. Код ответа: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании данных профиля: {e}")

    for re in reynolds:
        polar_url = f"http://airfoiltools.com/polar/text?polar=xf-{airfoil_name}-{re}"
        polar_file = os.path.join(save_folder, f"{airfoil_name}_Re_{re}_polar.txt")

        try:
            response = requests.get(polar_url, headers=headers, timeout=10)
            if response.status_code == 200:
                with open(polar_file, 'w') as file:
                    file.write(response.text)
                print(f"Данные поляры {airfoil_name} (Re={re}) сохранены в {polar_file}")
            else:
                print(f"Ошибка: Не удалось скачать данные поляры для Re={re}. Код ответа: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании данных поляры для Re={re}: {e}")


def load_airfoils_from_file(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        airfoils = [line.strip() for line in file if line.strip()]
    return airfoils

airfoil_names = load_airfoils_from_file("../data/airfoil_names.txt")
reynolds = [50000, 100000, 200000, 500000, 1000000]

for airfoil in airfoil_names:
    download_data(airfoil, reynolds)