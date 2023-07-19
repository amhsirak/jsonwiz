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

def test_set_value():
    data_copy = copy.deepcopy(data)
    # Test cases for setting new values
    set_value(data_copy, "person.name", "Alice")
    assert data_copy["person"]["name"] == "Alice"

    set_value(data_copy, "person.age", 25)
    assert data_copy["person"]["age"] == 25

    set_value(data_copy, "person.address.city", "San Francisco")
    assert data_copy["person"]["address"]["city"] == "San Francisco"

    # Test case for updating existing value
    set_value(data_copy, "items.0.name", "itemX")
    assert data_copy["items"][0]["name"] == "itemX"

def test_set_value_with_data_type():
    data_copy = copy.deepcopy(data)
    # Test cases for setting new values with data type
    set_value(data_copy, "person.age", "25", data_type="integer")
    assert data_copy["person"]["age"] == 25

    set_value(data_copy, "person.gender", "M", data_type="string")
    assert data_copy["person"]["gender"] == "M"

    set_value(data_copy, "person.is_employed", "True", data_type="boolean")
    assert data_copy["person"]["is_employed"] is True

    set_value(data_copy, "person.salary", "2500.50", data_type="float")
    assert data_copy["person"]["salary"] == 2500.50

def test_delete_value():
    data_copy = copy.deepcopy(data)
    # Test cases for deleting existing values
    delete_value(data_copy, "person.name")
    assert "name" not in data_copy["person"]

    delete_value(data_copy, "person.address.zipcode")
    assert "zipcode" not in data_copy["person"]["address"]

    delete_value(data_copy, "items.0.name")
    assert "name" not in data_copy["items"][0]

    # Test case for deleting non-existing value
    with pytest.raises(ValueError):
        delete_value(data_copy, "person.salary")

def test_validate_json():
    valid_json_str = '{"name": "Alice", "age": 30}' 
    assert validate_json(valid_json_str) is True
    invalid_json_str = '{"name": "Alice", "age": 30,}' # Trailing comma
    assert validate_json(invalid_json_str) is False

if __name__ == "__main__":
    pytest.main()
