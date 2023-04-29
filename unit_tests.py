import json
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_process_orders_completed():
    orders = [
        {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
        {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
    ]
    criterion = "completed"
    response = client.post(f"/solution?criterion={criterion}", content=json.dumps(orders))
    assert response.status_code == 200
    assert response.json() == {"total": 1299.69}

def test_process_orders_pending():
    orders = [
        {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
        {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
    ]
    criterion = "pending"
    response = client.post(f"/solution?criterion={criterion}", content=json.dumps(orders))
    assert response.status_code == 200
    assert response.json() == {"total": 999.9}

def test_process_orders_canceled():
    orders = [
        {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
        {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
    ]
    criterion = "canceled"
    response = client.post(f"/solution?criterion={criterion}", content=json.dumps(orders))
    assert response.status_code == 200
    assert response.json() == {"total": 99.96}
    
def test_not_positive_quantity():
    orders = [
        {"id": 1, "item": "Laptop", "quantity": -1, "price": 999.99, "status": "completed"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
        {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
        {"id": 4, "item": "Mouse", "quantity": 0, "price": 24.99, "status": "canceled"},
    ]
    criterion = "canceled"
    response = client.post(f"/solution?criterion={criterion}", content=json.dumps(orders))
    assert response.status_code == 422
    for msg in response.json()['detail']:
        assert msg['msg'] == "quantity field must be positive"
        
def test_not_positive_price():
    orders = [
        {"id": 1, "item": "Laptop", "quantity": 1, "price": -999.99, "status": "completed"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
        {"id": 3, "item": "Headphones", "quantity": 3, "price": 0, "status": "completed"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
    ]
    criterion = "canceled"
    response = client.post(f"/solution?criterion={criterion}", content=json.dumps(orders))
    assert response.status_code == 422
    for msg in response.json()['detail']:
        assert msg['msg'] == "price field must be positive"
        
def test_item_empty():
    orders = [
        {"id": 1, "item": "", "quantity": 1, "price": 999.99, "status": "completed"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
        {"id": 3, "item": "", "quantity": 3, "price": 99.90, "status": "completed"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
    ]
    criterion = "canceled"
    response = client.post(f"/solution?criterion={criterion}", content=json.dumps(orders))
    assert response.status_code == 422
    for msg in response.json()['detail']:
        assert msg['msg'] == "item field cannot be empty"