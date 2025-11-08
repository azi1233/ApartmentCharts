from scraper import extractor


class DivarRequest:
    def __init__(self, url: str, headers: dict, payload: dict):
        self.url = url
        self.headers = headers
        self.payload = payload

    def __repr__(self):
        return f"DivarRequest(url='{self.url}', headers={len(self.headers)} headers, payload keys={list(self.payload.keys())})"


#Mehran
    
url = "https://api.divar.ir/v8/mapview/viewport"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://divar.ir/",
    "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"
}

payload = {
    "city_ids": ["1"],
    "search_data": {
        "form_data": {
            "data": {
                "bbox": {
                    "repeated_float": {
                        "value": [
                            {"value": 51.4465828},
                            {"value": 35.7176476},
                            {"value": 51.4743233},
                            {"value": 35.7756462}
                        ]
                    }
                },
                "building-age": {"number_range": {"maximum": "20"}},
                "elevator": {"boolean": {"value": True}},
                "has-photo": {"boolean": {"value": True}},
                "parking": {"boolean": {"value": True}},
                "size": {"number_range": {"minimum": "75", "maximum": "120"}},
                "category": {"str": {"value": "apartment-sell"}},
                "districts": {"repeated_string": {"value": ["95"]}}
            }
        }
    },
    "camera_info": {
        "bbox": {
            "min_latitude": 35.717647,
            "min_longitude": 51.393049,
            "max_latitude": 35.775647,
            "max_longitude": 51.527854
        },
        "place_hash": "1|95|apartment-sell",
        "zoom": 11.342905675330188
    }
}

Mehran = DivarRequest(url,headers,payload)

extractor(Mehran)
