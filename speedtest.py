import sys
import time
from urllib.parse import urlparse

import requests

def is_valid_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https") and bool(result.netloc)
    except ValueError:
        return False

def request(url):
    start = time.perf_counter()

    response = requests.get(url)
    response.raise_for_status()

    end = time.perf_counter() - start
    size_mib = len(response.content) / 1024 / 1024

    return end, size_mib


def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <URL>")
        return

    url = sys.argv[1]

    if not is_valid_url(url):
        print("Ссылка не валидна")
        return

    count_requests = 10
    successful_requests = 0
    total_mib = 0.0
    total_seconds = 0.0

    for _ in range(count_requests):
        try:
            end, size_mib = request(url)
        except requests.RequestException as error:
            print(f"Ошибка запроса: {error}")
            continue

        total_mib += size_mib
        total_seconds += end
        successful_requests += 1

    if successful_requests == 0:
        print("Ни один запрос не выполнен успешно")
        return

    if (total_seconds <= 0): 
        total_seconds = 0.0

    average_time = total_seconds / successful_requests
    speed_mbit = (total_mib * 8) / total_seconds

    print(f"URL: {url}")
    print(f"Успешных запросов: {successful_requests} из {count_requests}")
    print(f"Общий объём: {total_mib:.2f} MiB")
    print(f"Общее время: {total_seconds:.2f} сек")
    print(f"Среднее время запроса: {average_time:.2f} сек")
    print(f"Средняя скорость: {speed_mbit:.2f} Mbit/s")


if __name__ == "__main__":
    main()