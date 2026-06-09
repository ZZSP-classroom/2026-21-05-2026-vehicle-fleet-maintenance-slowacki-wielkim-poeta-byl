import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_read_vehicle(client: AsyncClient):
    # Create vehicle
    response = await client.post("/api/vehicles/", json={
        "vin": "12345ABC12345ABCD",
        "make": "Ford",
        "model": "Transit",
        "year": 2020,
        "engine_type": "Diesel",
        "status": "ACTIVE"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["vin"] == "12345ABC12345ABCD"
    vehicle_id = data["id"]
    
    # Read vehicle
    response = await client.get(f"/api/vehicles/{vehicle_id}")
    assert response.status_code == 200
    assert response.json()["id"] == vehicle_id

@pytest.mark.asyncio
async def test_create_duplicate_vehicle(client: AsyncClient):
    # Create first vehicle
    await client.post("/api/vehicles/", json={
        "vin": "DUPLICATEVIN12345",
        "make": "Ford",
        "model": "Transit",
        "year": 2020
    })
    
    # Attempt to create duplicate
    response = await client.post("/api/vehicles/", json={
        "vin": "DUPLICATEVIN12345",
        "make": "Honda",
        "model": "Civic",
        "year": 2021
    })
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_nonexistent_vehicle(client: AsyncClient):
    response = await client.put("/api/vehicles/999", json={
        "vin": "12345ABC12345ABCD",
        "make": "Ford",
        "model": "Transit",
        "year": 2020
    })
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_maintenance_record_success(client: AsyncClient):
    # First create a vehicle
    resp_v = await client.post("/api/vehicles/", json={
        "vin": "MAINT123456789012",
        "make": "Honda",
        "model": "Civic",
        "year": 2018
    })
    v_id = resp_v.json()["id"]
    
    # Create maintenance
    resp_m = await client.post(f"/api/vehicles/{v_id}/maintenance", json={
        "vehicle_id": v_id,
        "description": "Oil Change",
        "cost": 50.25
    })
    assert resp_m.status_code == 200
    assert resp_m.json()["description"] == "Oil Change"
    
    # Verify unified view
    resp_view = await client.get(f"/api/vehicles/{v_id}/maintenance")
    assert resp_view.status_code == 200
    assert len(resp_view.json()["service_records"]) == 1

@pytest.mark.asyncio
async def test_create_maintenance_nonexistent_vehicle(client: AsyncClient):
    resp_m = await client.post("/api/vehicles/999/maintenance", json={
        "vehicle_id": 999,
        "description": "Oil Change",
        "cost": 50.25
    })
    assert resp_m.status_code == 404

@pytest.mark.asyncio
async def test_telemetry_batch_ingestion(client: AsyncClient):
    # Ensure vehicle exists
    resp_v = await client.post("/api/vehicles/", json={
        "vin": "TELEMETRY12345678",
        "make": "Toyota",
        "model": "Corolla",
        "year": 2021
    })
    v_id = resp_v.json()["id"]
    
    payload = [
        {"vehicle_id": v_id, "speed": 45, "engine_rpm": 2000, "coolant_temp": 90},
        {"vehicle_id": v_id, "speed": 50, "engine_rpm": 2200, "coolant_temp": 91}
    ]
    resp = await client.post("/api/telemetry/", json=payload)
    assert resp.status_code == 201

@pytest.mark.asyncio
async def test_telemetry_validation_error(client: AsyncClient):
    payload = [
        {"vehicle_id": 1, "speed": -10, "engine_rpm": 2000, "coolant_temp": 400}
    ]
    resp = await client.post("/api/telemetry/", json=payload)
    assert resp.status_code == 422

@pytest.mark.asyncio
async def test_reports_endpoint(client: AsyncClient):
    resp = await client.get("/api/reports/maintenance-costs")
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]

@pytest.mark.asyncio
async def test_inventory_endpoint(client: AsyncClient):
    resp = await client.post("/parts/", json={
        "part_number": "P-12345",
        "name": "Brake Pad",
        "stock_quantity": 100,
        "supplier": "AutoPartsCo"
    })
    assert resp.status_code == 200
    assert resp.json()["part_number"] == "P-12345"
    
    resp_get = await client.get("/parts/")
    assert resp_get.status_code == 200
    assert len(resp_get.json()) > 0
    
@pytest.mark.asyncio
async def test_inventory_reduce_stock(client: AsyncClient):
    resp = await client.post("/parts/", json={
        "part_number": "P-STOCKTEST",
        "name": "Wiper",
        "stock_quantity": 10,
        "supplier": "AutoPartsCo"
    })
    part_id = resp.json()["id"]
    
    # Reduce valid amount
    resp_reduce = await client.patch(f"/parts/{part_id}/reduce-stock?quantity=5")
    assert resp_reduce.status_code == 200
    assert resp_reduce.json()["stock_quantity"] == 5
    
    # Reduce below 0
    resp_reduce_fail = await client.patch(f"/parts/{part_id}/reduce-stock?quantity=10")
    assert resp_reduce_fail.status_code == 422
    
@pytest.mark.asyncio
async def test_auth_flow(client: AsyncClient):
    # Test unauthenticated access
    resp_unauth = await client.get("/api/auth/test-protected")
    assert resp_unauth.status_code == 401
    
    # Register
    await client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    
    # Login
    resp_login = await client.post("/api/auth/token", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert resp_login.status_code == 200
    token = resp_login.json()["access_token"]
    
    # Test authenticated access
    resp_auth = await client.get("/api/auth/test-protected", headers={"Authorization": f"Bearer {token}"})
    assert resp_auth.status_code == 200
    assert resp_auth.json()["message"] == "Hello testuser"
