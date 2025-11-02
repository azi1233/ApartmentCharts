#!/usr/bin/env python3
# scraper.py
# Run with: python3.13 scraper.py

import requests
import json
from datetime import datetime
from pathlib import Path
import sys
import re
from typing import Any, Dict, List, Optional

# ------------------------
# CONFIG: local price filter (applied after fetching posts)
# ------------------------
PRICE_FLOOR = 50_000_000
PRICE_CEILING = 300_000_000

# ------------------------
# EXACT PAYLOAD + HEADERS (unchanged)
# ------------------------
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

# ------------------------
# Output setup & helpers
# ------------------------
ts = datetime.now().strftime("%Y%m%d_%H%M%S")  # timestamp with date+time
out_dir = Path("./divar_results") / ts
out_dir.mkdir(parents=True, exist_ok=True)

def save_json(data: Any, filename: str):
    with open(out_dir / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ------------------------
# Parsers (for price, age, size)
# ------------------------
PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ENGLISH_DIGITS = "0123456789"

def persian_to_int(num_str: str) -> Optional[int]:
    if not isinstance(num_str, str):
        return None
    s = num_str
    for p, e in zip(PERSIAN_DIGITS, ENGLISH_DIGITS):
        s = s.replace(p, e)
    s = re.sub(r"[^\d]", "", s)
    return int(s) if s else None

WORDS_MAP = {
    "صفر":0, "یک":1, "دو":2, "سه":3, "چهار":4, "پنج":5, "شش":6, "هفت":7, "هشت":8, "نه":9,
    "ده":10, "یازده":11, "دوازده":12, "سیزده":13, "چهارده":14, "پانزده":15, "شانزده":16,
    "هفده":17, "هجده":18, "نوزده":19, "بیست":20, "سی":30, "چهل":40, "پنجاه":50, "شصت":60,
    "هفتاد":70, "هشتاد":80, "نود":90, "صد":100, "دویست":200, "سیصد":300, "چهارصد":400,
    "پانصد":500, "ششصد":600, "هفتصد":700, "هشتصد":800, "نهصد":900, "هزار":1000,
    "میلیون":1_000_000, "میلیارد":1_000_000_000
}

def words_to_number(text: str) -> Optional[int]:
    if not isinstance(text, str):
        return None
    text = text.replace("و", " ").replace("-", " ")
    total, temp = 0, 0
    for part in text.split():
        if part in WORDS_MAP:
            val = WORDS_MAP[part]
            if val >= 1000:
                temp = max(1, temp) * val
                total += temp
                temp = 0
            else:
                temp += val
    total += temp
    return total if total != 0 else None

def parse_price(text: str) -> Optional[int]:
    if not text:
        return None
    n = persian_to_int(text)
    if n is not None:
        if "میلیارد" in text:
            n *= 1_000_000_000
        elif "میلیون" in text:
            n *= 1_000_000
        return n
    n = words_to_number(text)
    if n is not None:
        if "میلیارد" in text:
            n *= 1_000_000_000
        elif "میلیون" in text:
            n *= 1_000_000
        return n
    return None

def parse_age(chips: List[Dict[str, Any]]) -> Optional[int]:
    if not chips:
        return None
    for chip in chips:
        title = chip.get("title", "")
        if not title:
            continue
        if "نوساز" in title:
            return 0
        if "سال" in title:
            m = re.search(r"[\d۰-۹]+", title)
            if m:
                return persian_to_int(m.group())
            w = words_to_number(title)
            if w is not None:
                return w
    return None

def parse_size(map_post: Dict[str, Any]) -> Optional[int]:
    for field in map_post.get("price_fields", []):
        title = field.get("title", "")
        if any(k in title for k in ["متراژ", "مساحت", "متری"]):
            val = field.get("value", "")
            s = persian_to_int(val) or words_to_number(val)
            if s:
                return s
    for chip in map_post.get("chips", []):
        title = chip.get("title", "")
        if any(k in title for k in ["متراژ", "متری"]):
            s = persian_to_int(title) or words_to_number(title)
            if s:
                return s
    return None

def avg(lst: List[float]) -> float:
    return sum(lst)/len(lst) if lst else 0.0

# ------------------------
# Make the request
# ------------------------
print(f"Posting to {url} (payload saved to {out_dir / 'request_payload.json'})")
save_json(payload, "request_payload.json")

try:
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status code: {resp.status_code}")
    resp.raise_for_status()
    data = resp.json()
except Exception as e:
    print("Error fetching posts:", e)
    sys.exit(1)

# ------------------------
# Extract posts only (keep all)
# ------------------------
posts = None
for key in ("posts", "widget_list", "items", "data"):
    if isinstance(data, dict) and isinstance(data.get(key), list):
        posts = data[key]
        break

if posts is None:
    # try to find first list-of-dicts anywhere in the JSON
    def find_first_list_of_dicts(obj):
        if isinstance(obj, list) and obj and isinstance(obj[0], dict):
            return obj
        if isinstance(obj, dict):
            for v in obj.values():
                r = find_first_list_of_dicts(v)
                if r:
                    return r
        return None
    posts = find_first_list_of_dicts(data)

if not posts:
    print("No posts array found in response JSON. Saving full response to response_full.json and exiting.")
    save_json(data, f"response_full_{ts}.json")
    sys.exit(0)

# Save the complete posts array with timestamp (keep all items)
posts_filename = f"posts_{ts}.json"
save_json(posts, posts_filename)
print(f"Saved posts ({len(posts)} items) -> {out_dir / posts_filename}")

# ------------------------
# Compute averages using only valid price-per-sqm values within floor/ceiling
# ------------------------
valid_prices = []
age_intervals = {"0-4": [], "5-9": [], "10-14": [], "15-20": []}
size_intervals = {"<80": [], "80-120": [], ">120": []}
age_size_matrix = {age: {"<80": [], "80-120": [], ">120": []} for age in age_intervals}

# we also create parsed_rows to provide a parsed view (but we still keep original posts file)
parsed_rows: List[Dict[str, Any]] = []

for post in posts:
    map_post = post.get("map_post_card", {}) or {}
    price_per_meter = None
    for field in map_post.get("price_fields", []):
        if "متری" in field.get("title", ""):
            price_per_meter = parse_price(field.get("value", ""))
            break
    age = parse_age(map_post.get("chips", []) or [])
    size = parse_size(map_post)

    parsed_rows.append({
        "id": post.get("id"),
        "title": post.get("title"),
        "price_per_sqm": price_per_meter,
        "age": age,
        "size": size,
    })

    if price_per_meter and PRICE_FLOOR <= price_per_meter <= PRICE_CEILING:
        valid_prices.append(price_per_meter)

        # classify age interval
        age_key = None
        if age is not None:
            if 0 <= age <= 4:
                age_key = "0-4"
            elif 5 <= age <= 9:
                age_key = "5-9"
            elif 10 <= age <= 14:
                age_key = "10-14"
            elif 15 <= age <= 20:
                age_key = "15-20"

        if age_key:
            age_intervals[age_key].append(price_per_meter)
            if size is not None:
                if size < 80:
                    age_size_matrix[age_key]["<80"].append(price_per_meter)
                elif 80 <= size <= 120:
                    age_size_matrix[age_key]["80-120"].append(price_per_meter)
                else:
                    age_size_matrix[age_key][">120"].append(price_per_meter)

        # size-only buckets
        if size is not None:
            if size < 80:
                size_intervals["<80"].append(price_per_meter)
            elif 80 <= size <= 120:
                size_intervals["80-120"].append(price_per_meter)
            else:
                size_intervals[">120"].append(price_per_meter)

summary = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_posts": len(posts),
    "valid_for_averages": len(valid_prices),
    "overall_avg_price_per_sqm": int(avg(valid_prices)) if valid_prices else 0,
    "age_intervals": {k: {"avg": int(avg(v)) if v else 0, "count": len(v)} for k, v in age_intervals.items()},
    "size_intervals": {k: {"avg": int(avg(v)) if v else 0, "count": len(v)} for k, v in size_intervals.items()},
    "age_size_matrix": {k: {kk: {"avg": int(avg(vv)) if vv else 0, "count": len(vv)} for kk, vv in v.items()} for k, v in age_size_matrix.items()},
}

# Save summary and parsed rows (rows are optional but helpful)
summary_filename = f"summary_{ts}.json"
rows_filename = f"rows_parsed_{ts}.json"
save_json(summary, summary_filename)
save_json(parsed_rows, rows_filename)

# Print human-readable summary
print("\n=== SUMMARY ===")
print(f"Timestamp: {summary['timestamp']}")
print(f"Total posts returned: {summary['total_posts']}")
print(f"Valid listings used for averages (price in {PRICE_FLOOR}–{PRICE_CEILING}): {summary['valid_for_averages']}")
print(f"Overall average price per sqm: {summary['overall_avg_price_per_sqm']:,} تومان\n")

print("Average by age intervals:")
for age, v in summary["age_intervals"].items():
    print(f"  {age} years: {v['avg']:,} تومان per sqm ({v['count']} listings)")

print("\nAverage by size intervals:")
for size, v in summary["size_intervals"].items():
    print(f"  {size} sqm: {v['avg']:,} تومان per sqm ({v['count']} listings)")

print("\nAge x Size matrix (avg price per sqm):")
for age, sizes in summary["age_size_matrix"].items():
    print(f" Age {age}:")
    for sz, data in sizes.items():
        print(f"   {sz}: {data['avg']:,} تومان ({data['count']})")

print(f"\nSaved files in: {out_dir}")
print(f"Posts JSON: {out_dir / posts_filename}")
print(f"Summary JSON: {out_dir / summary_filename}")
print(f"Parsed rows JSON: {out_dir / rows_filename}")
