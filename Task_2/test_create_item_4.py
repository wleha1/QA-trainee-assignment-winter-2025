import pytest
import requests

BASE_URL = "https://qa-internship.avito.com/api/1"

@pytest.mark.parametrize("seller_id, name, price, expected_status", [
    (999996, "Egor", 888, 200),  # Валидные значения
    (None, "Egor", 888, 400),  # sellerID = None
    (-1000, "Egor", 888, 400),  # Невалидный sellerID
    (0, "Egor", 888, 400),  # sellerID = 0
    (999996, None, 888, 400),  # name = None
    (999996, "Egor", -1000, 400),  # price < 0
    (999996, "Egor", 0, 400),  # price = 0
    (999996, "Egor", None, 400),  # price = None
    (1000000, "Egor", 888, 400)  # sellerID > 999999
])
def test_create_item(seller_id, name, price, expected_status):
    payload = {
        "sellerID": seller_id,
        "name": name,
        "price": price,
        "statistics": {
            "contacts": 3,
            "likes": 123,
            "viewCount": 12
        }
    }

    response = requests.post(f"{BASE_URL}/item", json=payload)

    # Проверка ожидаемого статуса
    assert response.status_code == expected_status, f"Ожидался статус {expected_status}, но получен {response.status_code}"

    # Если статус 200, проверяем полученные данные
    if response.status_code == 200:
        data = response.json()

        print("Ответные данные:", data)

        assert "status" in data, "Ответ должен содержать поле 'status'"

        status_message = data["status"]

        item_id = status_message.split(" - ")[-1]

        assert item_id, "Ответ должен содержать ID в статусе"

        get_response = requests.get(f"{BASE_URL}/item/{item_id}")
        assert get_response.status_code == 200, f"Ожидался статус 200, но получен {get_response.status_code}"

        item_data = get_response.json()

        print("Данные товара:", item_data)

        if isinstance(item_data, list):
            item_data = item_data[0]

        assert isinstance(item_data, dict), f"Ожидалось, что item_data будет словарем, а получен {type(item_data)}"

        assert item_data["name"] == payload["name"], f"Ожидалось имя {payload['name']}, а получено {item_data['name']}"
        assert item_data["price"] == payload["price"], f"Ожидалась цена {payload['price']}, а получена {item_data['price']}"
        assert item_data["sellerId"] == payload["sellerID"], f"Ожидался sellerId {payload['sellerID']}, а получен {item_data['sellerId']}"

        assert item_data["statistics"]["likes"] == payload["statistics"]["likes"], \
            f"Ожидались лайки {payload['statistics']['likes']}, а получено {item_data['statistics']['likes']}"
        assert item_data["statistics"]["contacts"] == payload["statistics"]["contacts"], \
            f"Ожидались контакты {payload['statistics']['contacts']}, а получено {item_data['statistics']['contacts']}"
        assert item_data["statistics"]["viewCount"] == payload["statistics"]["viewCount"], \
            f"Ожидалось количество просмотров {payload['statistics']['viewCount']}, а получено {item_data['statistics']['viewCount']}"
