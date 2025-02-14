import pytest
import requests

BASE_URL = "https://qa-internship.avito.com/api/1"

@pytest.mark.parametrize("item_id, expected_status", [
    ("0cd4183f-a699-4486-83f8-b513dfde477a", 200),  # ID Существует
    ("", 400),
    (None, 400),
    ("@#$%", 400),
    (-10, 400),
    ("0cd4183f-a699-4486-83f8-b513dfde4779", 404)  # Несуществующий ID
])
def test_get_item_by_id(item_id, expected_status):
    response = requests.get(f"{BASE_URL}/item/{item_id}")
    assert response.status_code == expected_status, f"Ожидался статус {expected_status}, но получен {response.status_code}"

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list), f"Ожидался список, но получен {type(data)}: {data}"
        assert len(data) > 0, "Ответный список пуст"
        
        item_data = data[0]
        assert isinstance(item_data, dict), f"Ожидался словарь, но получен {type(item_data)}"
        
        assert "id" in item_data, f"Отсутствует 'id' в данных элемента: {item_data}"
        assert isinstance(item_data["id"], str), f"Ожидался строковый тип для 'id', но получен {type(item_data['id'])}"
        
        assert "sellerId" in item_data, f"Отсутствует 'sellerId' в данных элемента: {item_data}"
        assert isinstance(item_data["sellerId"], int), f"Ожидался целочисленный тип для 'sellerId', но получен {type(item_data['sellerId'])}"
        
        assert "name" in item_data, f"Отсутствует 'name' в данных элемента: {item_data}"
        assert isinstance(item_data["name"], str), f"Ожидался строковый тип для 'name', но получен {type(item_data['name'])}"
        
        assert "price" in item_data, f"Отсутствует 'price' в данных элемента: {item_data}"
        assert isinstance(item_data["price"], int), f"Ожидался целочисленный тип для 'price', но получен {type(item_data['price'])}"
        
        assert "statistics" in item_data, f"Отсутствует 'statistics' в данных элемента: {item_data}"
        assert isinstance(item_data["statistics"], dict), f"Ожидался словарь для 'statistics', но получен {type(item_data['statistics'])}"
        
        assert "likes" in item_data["statistics"], f"Отсутствует 'likes' в статистике: {item_data['statistics']}"
        assert isinstance(item_data["statistics"]["likes"], int), f"Ожидался целочисленный тип для 'likes', но получен {type(item_data['statistics']['likes'])}"
        
        assert "contacts" in item_data["statistics"], f"Отсутствует 'contacts' в статистике: {item_data['statistics']}"
        assert isinstance(item_data["statistics"]["contacts"], int), f"Ожидался целочисленный тип для 'contacts', но получен {type(item_data['statistics']['contacts'])}"
        
        assert "viewCount" in item_data["statistics"], f"Отсутствует 'viewCount' в статистике: {item_data['statistics']}"
        assert isinstance(item_data["statistics"]["viewCount"], int), f"Ожидался целочисленный тип для 'viewCount', но получен {type(item_data['statistics']['viewCount'])}"
        
        assert "createdAt" in item_data, f"Отсутствует 'createdAt' в данных элемента: {item_data}"
        assert isinstance(item_data["createdAt"], str), f"Ожидался строковый тип для 'createdAt', но получен {type(item_data['createdAt'])}"

    elif response.status_code in [400, 404]:
        data = response.json()
        assert "result" in data, "Отсутствует поле 'result' в ответе"
        assert "message" in data["result"], "Отсутствует сообщение об ошибке в 'result'"
        assert isinstance(data["result"]["message"], str), f"Ожидался строковый тип для 'message', но получен {type(data['result']['message'])}"
        assert "status" in data, "Отсутствует поле 'status' в ответе"
        assert isinstance(data["status"], str), f"Ожидался строковый тип для 'status', но получен {type(data['status'])}"

        messages = data["result"].get("messages")
        assert messages is None or isinstance(messages, dict), \
            f"Ожидался None или словарь для 'messages', но получен {type(messages)}"
