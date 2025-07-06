import requests


BASE_API_URL = "http://127.0.0.1:5011"

def get_data_v1(page, limit, filters):
    try:
        params = {
            "page": page,
            "limit": limit
        }
        params.update(filters)
        response = requests.get(f"{BASE_API_URL}/data/tr-raw-scrap-data", params = params)
        response.raise_for_status()
        data = response.json()
        print(f"Menampilkan halaman {data['page']} (limit {data['limit']}):\n")
        for product in data["data"]:
            print(f"{product['id']} - {product['name']} - {product['price']}")
    except requests.RequestException as e:
        print(f"Terjadi error saat mengakses API: {e}")
    except ValueError:
        print("Respons bukan JSON valid.")


if __name__ == "__main__":
    filters = {
        "id_lt": 3
    }
    get_data_v1(page = 1, limit = 5, filters = filters)
