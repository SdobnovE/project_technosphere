import requests
import json
key = "dict.1.1.20191128T185228Z.0bc4a1fee579c4ce.217d9bd27cf4c55d564e01c5a747c1c7276d797d"

class DICT_YANDEX_WEB_API:

    def __init__(self, key=key, num_sin=3, lang="ru-ru"):
        self.lang = lang
        self.key = key
        self.num_sin = num_sin
        self.addr = ("https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key="
                     + self.key + "&lang=ru-ru&text=")
       
    def parse_json(self, response):
        
            pr = json.loads(response.text)
            if len(pr["def"]) == 0:
                return None
            res = json.loads(response.text)["def"][0]["tr"]
            
            ln = len(res)
            result = []
            for i in range(min(ln, self.num_sin)):
                result.append(res[i]["text"] + " ")
            return "".join(result)
    
    def get_sinonims(self, word):
        response = ""
        for i in range(5):
            response = requests.get(self.addr + word)
            if response.status_code == 200:
                break
            elif response.status_code == 401:
                print("Невалидный ключ")
                return None
            elif response.status_code == 402:
                print("Ключ заблочен")
                return None
            elif response.status_code == 403:
                print("Превышено суточное ограничение на количество запросов.")
                return None
            elif response.status_code == 413:
                print("Превышен размер текста")
                return None
            elif response.status_code == 501:
                print("Заданное напрвление не поддерживается")
                return None
        if response.status_code != 200:
            print("ERROR")
            return None
        
        return self.parse_json(response)
