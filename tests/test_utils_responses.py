import json
from fastapi_mctools.utils.responses import ResponseInterFace


def test_response_interface_to_dict():
    result = "success"
    kwargs = {"key1": "value1", "key2": "value2"}
    response = ResponseInterFace(result, **kwargs)
    expected_dict = {"result": result, "key1": "value1", "key2": "value2"}
    assert response.to_dict() == expected_dict


def test_response_interface_to_str():
    result = "success"
    kwargs = {"key1": "value1", "key2": "value2"}
    response = ResponseInterFace(result, **kwargs)
    response_to_str = response.to_str()
    response_dict = json.loads(response_to_str)

    assert response_dict == {"result": result, "key1": "value1", "key2": "value2"}


def test_response_interface_unpacking():
    result = "success"
    kwargs = {"key1": "value1", "key2": "value2"}
    response = ResponseInterFace(result, **kwargs)
    response_dict = dict(**response)
    assert response_dict == {"result": result, "key1": "value1", "key2": "value2"}
