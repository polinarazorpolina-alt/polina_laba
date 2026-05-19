import requests

def get_coordinates(city_name):
    """Получение координат города через Geocoding API Open-Meteo."""
    # Правильный URL для геокодинга
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "ru",
        "format": "json"
    }

    try:
        response = requests.get(geo_url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and data["results"]:
                result = data["results"][0]
                return {
                    "lat": result["latitude"],
                    "lon": result["longitude"],
                    "name": result["name"],
                    "country": result.get("country", ""),
                }
    except Exception as e:
        print(f"Ошибка при запросе координат: {e}")
    return None

def get_weather(lat, lon):
    """Получение текущей погоды через Forecast API Open-Meteo."""
    # Правильный URL для прогноза
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"
    }

    try:
        response = requests.get(weather_url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get("current_weather")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при получении погоды: {e}")
    return None

def main():
    print("=== Консольное погодное приложение ===")
    city_name = input("Введите наименование города: ").strip()

    if not city_name:
        print("Ошибка: Название города не может быть пустым.")
        return

    print("\nПоиск города...")
    location = get_coordinates(city_name)

    if not location:
        print("Ошибка: Город не найден или API недоступно.")
        return

    print(f"Найден объект: {location['name']} ({location['country']})")
    print("Получение данных о погоде...")

    weather = get_weather(location["lat"], location["lon"])

    if not weather:
        print("Ошибка: Не удалось получить данные о погоде.")
        return

    # Структурированный вывод
    print("\n" + "=" * 35)
    print(f" ТЕКУЩАЯ ПОГОДА В Г. {location['name'].upper()}")
    print("=" * 35)
    print(f" Температура:    {weather['temperature']} °C")
    print(f" Скорость ветра: {weather['windspeed']} км/ч")
    print(f" Направление:    {weather['winddirection']}°")
    print("=" * 35)

if __name__ == "__main__":
    main()