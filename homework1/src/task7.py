import requests 

def get_status_code(url):
    response = requests.get(url)
    return response.status_code


if __name__ == "__main__":
    print(get_status_code("https://example.com"))
