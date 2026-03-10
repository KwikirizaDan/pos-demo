import httpx
import time
import subprocess
import os

def test_pos_app():
    # Start the server
    process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    time.sleep(3)

    try:
        with httpx.Client(base_url="http://127.0.0.1:8000") as client:
            # 1. Test root endpoint
            response = client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "Welcome to the POS Demo API"}
            print("Root endpoint: OK")

            # 2. Create an item
            item_data = {
                "name": "Coffee",
                "description": "Delicious dark roast",
                "price": 2.5,
                "inventory_quantity": 100
            }
            response = client.post("/items/", json=item_data)
            assert response.status_code == 200
            item = response.json()
            assert item["name"] == "Coffee"
            item_id = item["id"]
            print(f"Create item: OK (ID: {item_id})")

            # 3. Read items
            response = client.get("/items/")
            assert response.status_code == 200
            assert len(response.json()) >= 1
            print("Read items: OK")

            # 4. Create a sale
            sale_data = {
                "items": [
                    {"item_id": item_id, "quantity": 2}
                ]
            }
            response = client.post("/sales/", json=sale_data)
            assert response.status_code == 200
            sale = response.json()
            assert sale["total_amount"] == 5.0
            assert len(sale["items"]) == 1
            print("Create sale: OK")

            # 5. Check inventory update
            response = client.get(f"/items/{item_id}")
            assert response.status_code == 200
            assert response.json()["inventory_quantity"] == 98
            print("Inventory update: OK")

            # 6. Read sales
            response = client.get("/sales/")
            assert response.status_code == 200
            assert len(response.json()) >= 1
            print("Read sales: OK")

    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    try:
        test_pos_app()
        print("All tests passed!")
    except Exception as e:
        print(f"Tests failed: {e}")
        exit(1)
