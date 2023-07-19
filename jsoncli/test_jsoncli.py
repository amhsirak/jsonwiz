import pytest
import copy
from jsoncli import get_value, set_value, delete_value, validate_json

data = {
    "person": {
        "name": "John",
        "age": 30,
        "address": {
            "city": "New York",
            "zipcode": "10001",
            "street": "Main Street"
        },
        "gender": "F"
    },
    "items": [
        {
            "name": "item1",
            "price": 10
        },
        {
            "name": "item2",
            "price": 20
        }
    ]
}

def test_get_value():
    data_copy = copy.deepcopy(data)
    # Test cases for valid keys
    assert get_value(data_copy, "person.name") == "John"
    assert get_value(data_copy, "person.address.zipcode") == "10001"
    assert get_value(data_copy, "items.0.name") == "item1"
    assert get_value(data_copy, "items.1.price") == 20

    # Test case for invalid key
    assert get_value(data_copy, "person.salary") is None

if __name__ == "__main__":
    pytest.main()
