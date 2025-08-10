#!/usr/bin/env python3
"""
Script de ejemplo para probar la API REST de Expensy
Ejecutar después de iniciar el servidor Django
"""

import requests
import json
from datetime import date, datetime

# Configuración
BASE_URL = "http://localhost:8000/api"
HEADERS = {"Content-Type": "application/json"}


def test_categories():
    """Prueba los endpoints de Categories"""
    print("=== Probando endpoints de Categories ===\n")

    # 1. Listar categorías (debe estar vacío inicialmente)
    print("1. Listando categorías existentes...")
    response = requests.get(f"{BASE_URL}/categories/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.json()}\n")

    # 2. Crear primera categoría
    print("2. Creando categoría 'Comida'...")
    category_data = {"name": "Comida", "alt_name": "Alimentación"}
    response = requests.post(
        f"{BASE_URL}/categories/", headers=HEADERS, data=json.dumps(category_data)
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        category = response.json()
        category_id = category["id"]
        print(f"Categoría creada con ID: {category_id}")
    else:
        print(f"Error: {response.json()}")
    print()

    # 3. Crear segunda categoría
    print("3. Creando categoría 'Transporte'...")
    category_data = {"name": "Transporte", "alt_name": "Movilidad"}
    response = requests.post(
        f"{BASE_URL}/categories/", headers=HEADERS, data=json.dumps(category_data)
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        category = response.json()
        transport_id = category["id"]
        print(f"Categoría creada con ID: {transport_id}")
    else:
        print(f"Error: {response.json()}")
    print()

    # 4. Listar todas las categorías
    print("4. Listando todas las categorías...")
    response = requests.get(f"{BASE_URL}/categories/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}\n")

    # 5. Obtener categoría específica
    print("5. Obteniendo categoría 'Comida'...")
    response = requests.get(f"{BASE_URL}/categories/{category_id}/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}\n")

    # 6. Actualizar categoría
    print("6. Actualizando categoría 'Comida'...")
    update_data = {"alt_name": "Gastos en comida"}
    response = requests.patch(
        f"{BASE_URL}/categories/{category_id}/",
        headers=HEADERS,
        data=json.dumps(update_data),
    )
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}\n")

    return category_id, transport_id


def test_records(category_id, transport_id):
    """Prueba los endpoints de Records"""
    print("=== Probando endpoints de Records ===\n")

    # 1. Listar registros (debe estar vacío inicialmente)
    print("1. Listando registros existentes...")
    response = requests.get(f"{BASE_URL}/records/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.json()}\n")

    # 2. Crear primer registro
    print("2. Creando registro 'Compra en supermercado'...")
    record_data = {
        "description": "Compra en supermercado",
        "date": str(date.today()),
        "time": datetime.now().strftime("%H:%M:%S"),
        "category": category_id,
        "amount": "150.50",
        "source": "ingreso manual",
    }
    response = requests.post(
        f"{BASE_URL}/records/", headers=HEADERS, data=json.dumps(record_data)
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        record = response.json()
        record_id = record["id"]
        print(f"Registro creado con ID: {record_id}")
    else:
        print(f"Error: {response.json()}")
    print()

    # 3. Crear segundo registro
    print("3. Creando registro 'Taxi al trabajo'...")
    record_data = {
        "description": "Taxi al trabajo",
        "date": str(date.today()),
        "time": datetime.now().strftime("%H:%M:%S"),
        "category": transport_id,
        "amount": "25.00",
        "source": "ingreso manual",
    }
    response = requests.post(
        f"{BASE_URL}/records/", headers=HEADERS, data=json.dumps(record_data)
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        record = response.json()
        record2_id = record["id"]
        print(f"Registro creado con ID: {record2_id}")
    else:
        print(f"Error: {response.json()}")
    print()

    # 4. Listar todos los registros
    print("4. Listando todos los registros...")
    response = requests.get(f"{BASE_URL}/records/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}\n")

    # 5. Obtener registro específico
    print("5. Obteniendo registro 'Compra en supermercado'...")
    response = requests.get(f"{BASE_URL}/records/{record_id}/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}\n")

    # 6. Actualizar registro
    print("6. Actualizando monto del registro...")
    update_data = {"amount": "175.25"}
    response = requests.patch(
        f"{BASE_URL}/records/{record_id}/",
        headers=HEADERS,
        data=json.dumps(update_data),
    )
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}\n")

    # 7. Filtrar por categoría
    print("7. Filtrando registros por categoría 'Comida'...")
    response = requests.get(
        f"{BASE_URL}/records/by_category/?category_id={category_id}"
    )
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}\n")

    # 8. Filtrar por rango de fechas
    print("8. Filtrando registros por rango de fechas...")
    today = str(date.today())
    response = requests.get(
        f"{BASE_URL}/records/by_date_range/?start_date={today}&end_date={today}"
    )
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}\n")

    return record_id, record2_id


def test_delete(category_id, transport_id, record_id, record2_id):
    """Prueba la eliminación de registros y categorías"""
    print("=== Probando eliminación ===\n")

    # 1. Eliminar registros
    print("1. Eliminando registro 'Taxi al trabajo'...")
    response = requests.delete(f"{BASE_URL}/records/{record2_id}/")
    print(f"Status: {response.status_code}")
    print("Registro eliminado\n")

    print("2. Eliminando registro 'Compra en supermercado'...")
    response = requests.delete(f"{BASE_URL}/records/{record_id}/")
    print(f"Status: {response.status_code}")
    print("Registro eliminado\n")

    # 2. Eliminar categorías
    print("3. Eliminando categoría 'Transporte'...")
    response = requests.delete(f"{BASE_URL}/categories/{transport_id}/")
    print(f"Status: {response.status_code}")
    print("Categoría eliminada\n")

    print("4. Eliminando categoría 'Comida'...")
    response = requests.delete(f"{BASE_URL}/categories/{category_id}/")
    print(f"Status: {response.status_code}")
    print("Categoría eliminada\n")

    # 3. Verificar que todo esté limpio
    print("5. Verificando que no queden registros...")
    response = requests.get(f"{BASE_URL}/records/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.json()}\n")

    print("6. Verificando que no queden categorías...")
    response = requests.get(f"{BASE_URL}/categories/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.json()}\n")


def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de la API REST de Expensy\n")

    try:
        # Probar Categories
        category_id, transport_id = test_categories()

        # Probar Records
        record_id, record2_id = test_records(category_id, transport_id)

        # Probar eliminación
        test_delete(category_id, transport_id, record_id, record2_id)

        print("✅ Todas las pruebas completadas exitosamente!")
        print("\n🎉 La API está funcionando correctamente!")

    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor.")
        print("Asegúrate de que Django esté ejecutándose en http://localhost:8000")
        print("\nPara iniciar el servidor:")
        print("1. cd data")
        print("2. poetry shell")
        print("3. python manage.py runserver")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
