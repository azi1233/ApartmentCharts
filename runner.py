from scraper import extractor
from scraper import DivarRequest
from ModifiedScraper import extractor2

def run():
    
    
    
    
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
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
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
    
    paths ="Seyyed-Khandan_Araghi_Khaje-Abdollah_Mehran"
    
    Mehran = DivarRequest(url,headers,payload,paths)
    
    extractor(Mehran)
    
    
    
    
    ##Gisha
    
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
                                {"value": 51.3350372},
                                {"value": 35.7241974},
                                {"value": 51.4088402},
                                {"value": 35.750042}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["88"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.724198,
                "min_longitude": 51.335037,
                "max_latitude": 35.750043,
                "max_longitude": 51.408842
            },
            "place_hash": "1|88|apartment-sell",
            "zoom": 12.899449156018573
        }
    }
    
    paths ="Gisha"
    
    gisha = DivarRequest(url,headers,payload,paths)
    extractor(gisha)
    
    
    
    ##ShahrAra
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
                                {"value": 51.3174362},
                                {"value": 35.7004204},
                                {"value": 51.4182167},
                                {"value": 35.7357216}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["202"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.700421,
                "min_longitude": 51.317436,
                "max_latitude": 35.735721,
                "max_longitude": 51.418215
            },
            "place_hash": "1|202|apartment-sell",
            "zoom": 12.450042235879172
        }
    }
    
    paths ="ShahrAra"
    
    shahrara = DivarRequest(url,headers,payload,paths)
    extractor(shahrara)
    
    
    
    
    ##TehranVilla
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
                                {"value": 51.3441467},
                                {"value": 35.7074127},
                                {"value": 51.3795242},
                                {"value": 35.7357025}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["201"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.709418,
                "min_longitude": 51.346308,
                "max_latitude": 35.737709,
                "max_longitude": 51.381686
            },
            "place_hash": "1|201|apartment-sell",
            "zoom": 12.450042235879172
        }
    }
    
    paths ="TehranVilla"
    
    tehranvilla = DivarRequest(url,headers,payload,paths)
    extractor(tehranvilla)
    
    
    ##YousefAbad_up
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
                                {"value": 51.378773},
                                {"value": 35.717261},
                                {"value": 51.425958},
                                {"value": 35.754989}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["90"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.717261,
                "min_longitude": 51.378773,
                "max_latitude": 35.754989,
                "max_longitude": 51.425958
            },
            "place_hash": "1|90|apartment-sell",
            "zoom": 12.7
        }
    }
    
    paths ="YousefAbad_up"
    
    YousefAbad_up = DivarRequest(url,headers,payload,paths)
    extractor(YousefAbad_up)
    
################################# second calculation (more precise)




 #Mehran_new
        
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
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
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
    
    paths ="Seyyed-Khandan_Araghi_Khaje-Abdollah_Mehran_new"
    
    Mehran_new = DivarRequest(url,headers,payload,paths)
    
    extractor2(Mehran_new)
    
    
    
    
    ##Gisha_new
    
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
                                {"value": 51.3350372},
                                {"value": 35.7241974},
                                {"value": 51.4088402},
                                {"value": 35.750042}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["88"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.724198,
                "min_longitude": 51.335037,
                "max_latitude": 35.750043,
                "max_longitude": 51.408842
            },
            "place_hash": "1|88|apartment-sell",
            "zoom": 12.899449156018573
        }
    }
    
    paths ="Gisha_new"
    
    gisha_new = DivarRequest(url,headers,payload,paths)
    extractor2(gisha_new)
    
    
    
    ##ShahrAra_new
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
                                {"value": 51.3174362},
                                {"value": 35.7004204},
                                {"value": 51.4182167},
                                {"value": 35.7357216}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["202"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.700421,
                "min_longitude": 51.317436,
                "max_latitude": 35.735721,
                "max_longitude": 51.418215
            },
            "place_hash": "1|202|apartment-sell",
            "zoom": 12.450042235879172
        }
    }
    
    paths ="ShahrAra_new"
    
    shahrara_new = DivarRequest(url,headers,payload,paths)
    extractor2(shahrara_new)
    
    
    
    
    ##TehranVilla_new
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
                                {"value": 51.3441467},
                                {"value": 35.7074127},
                                {"value": 51.3795242},
                                {"value": 35.7357025}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["201"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.709418,
                "min_longitude": 51.346308,
                "max_latitude": 35.737709,
                "max_longitude": 51.381686
            },
            "place_hash": "1|201|apartment-sell",
            "zoom": 12.450042235879172
        }
    }
    
    paths ="TehranVilla_new"
    
    tehranvilla_new = DivarRequest(url,headers,payload,paths)
    extractor2(tehranvilla_new)
    
    
    ##YousefAbad_up_new
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
                                {"value": 51.378773},
                                {"value": 35.717261},
                                {"value": 51.425958},
                                {"value": 35.754989}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["90"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.717261,
                "min_longitude": 51.378773,
                "max_latitude": 35.754989,
                "max_longitude": 51.425958
            },
            "place_hash": "1|90|apartment-sell",
            "zoom": 12.7
        }
    }
    
    paths ="YousefAbad_up_new"
    
    YousefAbad_up_new = DivarRequest(url,headers,payload,paths)
    extractor2(YousefAbad_up_new)
    
    
    ######
    
    ##Javadie_new
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
                                {"value": 51.376478},
                                {"value": 35.640342},
                                {"value": 51.417136},
                                {"value": 35.663281}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["265"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.640342,  
                "min_longitude": 51.376478,
                "max_latitude": 35.663281,
                "max_longitude": 51.417136
            },
            "place_hash": "1|265|apartment-sell",
            "zoom": 12.7
        }
    }
    
    paths ="Javadieh_new"
    
    Javadieh_new = DivarRequest(url,headers,payload,paths)
    extractor2(Javadieh_new)
    
    
       ##HosseinAbad_new
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
                                {"value": 51.466303},
                                {"value": 35.769012},
                                {"value": 51.498038},
                                {"value": 35.786889}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["1025"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.769012, 
                "min_longitude": 51.466303,  
                "max_latitude": 35.786889,  
                "max_longitude": 51.498038  

            },
            "place_hash": "1|1025|apartment-sell",
            "zoom": 12.7
        }
    }
    
    paths ="HosseinAbad_new"
    
    HosseinAbad_new = DivarRequest(url,headers,payload,paths)
    extractor2(HosseinAbad_new)
    
    
    
    
    
    
    
    
    
    
    
        ##Dr_Hooshyar_new
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
                                {"value": 51.3384247},
                                {"value": 35.6879234},
                                {"value": 51.3614235},
                                {"value": 35.7008896}
                            ]
                        }
                    },
                    "building-age": {"number_range": {"maximum": "20"}},
                    "elevator": {"boolean": {"value": True}},
                    "has-photo": {"boolean": {"value": True}},
                    "parking": {"boolean": {"value": True}},
                    "size": {"number_range": {"minimum": "60", "maximum": "150"}},
                    "category": {"str": {"value": "apartment-sell"}},
                    "districts": {"repeated_string": {"value": ["1029"]}}
                }
            }
        },
        "camera_info": {
            "bbox": {
                "min_latitude": 35.687028,
                "min_longitude": 51.33617,
                "max_latitude": 35.701785,
                "max_longitude": 51.362339
            },
            "place_hash": "1|1029|apartment-sell",
            "zoom": 12.7
        }
    }
    
    paths ="Dr_Hooshyar_new"
    
    Dr_Hooshyar_new = DivarRequest(url,headers,payload,paths)
    extractor2(Dr_Hooshyar_new)