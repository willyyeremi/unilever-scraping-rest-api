import requests


BASE_API_URL = "http://127.0.0.1:5000"

def get_games_v1(page, limit, **kwargs):
    try:
        params = {
            "page": page,
            "limit": limit
        }
        params.update(kwargs)
        response = requests.get(f"{BASE_API_URL}/v1/games", params = params)
        response.raise_for_status()
        data = response.json()
        print(f"Menampilkan halaman {data['page']} (limit {data['limit']}):\n")
        for game in data["data"]:
            print(f"- {game['id']}: {game['game_title']} (active: {game['is_active']})")
    except requests.RequestException as e:
        print(f"Terjadi error saat mengakses API: {e}")
    except ValueError:
        print("Respons bukan JSON valid.")


if __name__ == "__main__":
    get_games_v1(page = 1, limit = 5, id = 1)
