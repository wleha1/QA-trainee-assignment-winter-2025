import pytest
import requests

BASE_URL = "https://qa-internship.avito.com/api/1"

@pytest.mark.parametrize("seller_id, expected_status", [
    (999997, 200),  # Валидный sellerID
    (None, 400),  # sellerID = None
    (-999997, 400),  # Отрицательный sellerID
    ("@#$%", 400),  # Невалидный sellerID
    ("", 400),  # Пустой sellerID
    (0, 400)  # sellerID равен 0
])
def test_get_items_by_seller(seller_id, expected_status):
    """ Проверяем получение объявлений по sellerID с разными параметрами """
    
    url = f"{BASE_URL}/{seller_id}/item" if seller_id is not None else f"{BASE_URL}/None/item"
    
    response = requests.get(url)

    assert response.status_code == expected_status, f"Ожидался статус {expected_status}, но получен {response.status_code}"

    # Получаем данные из ответа
    data = response.json()

    # Если статус 200, проверяем структуру ответа
    if expected_status == 200:
        assert isinstance(data, list), "Ожидался список объявлений"
        for item in data:
            assert isinstance(item, dict), "Каждое объявление должно быть объектом"
            assert "sellerId" in item, "Объявление должно содержать поле 'sellerId'"
            assert item["sellerId"] == seller_id, f"Ожидался sellerId {seller_id}, но получен {item['sellerId']}"
    
    else:
        assert "result" in data, "Ожидался ключ 'result' в ошибке"
        assert "message" in data["result"], "Ожидалось сообщение об ошибке"
        assert isinstance(data["result"]["message"], str), "Поле 'message' должно быть строкой"
