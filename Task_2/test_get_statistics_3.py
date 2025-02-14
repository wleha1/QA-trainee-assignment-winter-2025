import pytest
import requests

BASE_URL = "https://qa-internship.avito.com/api/1"

@pytest.mark.parametrize("item_id, expected_status", [
    ("0cd4183f-a699-4486-83f8-b513dfde477a", 200),  # ID существует
    (None, 400),
    (-1, 400),
    ("@#$%", 400),
    ("0cd4183f-a699-4486-83f8-b513dfde4779", 404)  # Несуществующий ID
])
def test_get_statistics_by_id(item_id, expected_status):
    response = requests.get(f"{BASE_URL}/statistic/{item_id}")
    
    assert response.status_code == expected_status

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert "contacts" in data[0] and isinstance(data[0]["contacts"], int)
        assert "likes" in data[0] and isinstance(data[0]["likes"], int)
        assert "viewCount" in data[0] and isinstance(data[0]["viewCount"], int)

    elif response.status_code in [400, 404]:
        data = response.json()
        assert "result" in data
        result = data["result"]
        
        messages = result.get("messages", None)
        assert isinstance(messages, (dict, type(None))), f"Expected 'messages' to be a dict or None, got {type(messages)}"
        
        assert "message" in result
        assert isinstance(result["message"], str)
        
        assert "status" in data
        assert isinstance(data["status"], str)
