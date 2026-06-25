#!/usr/bin/env python3
# scraper.py
# Run with: python3.13 scraper.py

import requests
import json
import gzip
from datetime import datetime, timedelta
from pathlib import Path
import sys
import re
from typing import Any, Dict, List, Optional
import time

# ------------------------
# Config: tweak as needed
# ------------------------
PRICE_FLOOR = 70_000_000
PRICE_CEILING = 900_000_000
REQUEST_TIMEOUT = 30
PAGE_SIZE_GUESS = 200
RATE_LIMIT_SLEEP = 0.12  # small delay between requests to be polite
POSTS_RETENTION_DAYS = 7  # Keep posts_collected_*.json and omitted_items_*.json files for 7 days

class DivarRequest:
    def __init__(self, url: str, headers: dict, payload: dict, path: str):
        self.url = url
        self.headers = headers
        self.payload = payload
        self.path = path

def extractor(diverRequest: DivarRequest):

    url = diverRequest.url
    headers = diverRequest.headers
    payload = diverRequest.payload
    path_d = diverRequest.path

    # ------------------------
    # Output setup & helpers
    # ------------------------
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("./divar_results/" + path_d) / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    def save_json(data: Any, filename: str) -> str:
        gz_filename = filename.replace('.json', '.json.gz')
        with gzip.open(out_dir / gz_filename, 'wt', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        return gz_filename

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
        # attempts to find size in price_fields and chips exactly like your original
        #for field in map_post.get("price_fields", []):
        #    title = field.get("title", "")
        #    if any(k in title for k in ["متراژ", "مساحت", "متر" , "زیربنا" , "زیر بنا"]):
        #        val = field.get("value", "")
        #        s = persian_to_int(val) or words_to_number(val)
        #        if s:
        #            return s
        for chip in map_post.get("chips", []):
            title = chip.get("title", "")
            if any(k in title for k in ["متراژ", "مساحت", "متر" , "زیربنا" , "زیر بنا"]):
                s = persian_to_int(title) or words_to_number(title)
                if s:
                    return s
        return None

    def avg(lst: List[float]) -> float:
        return sum(lst)/len(lst) if lst else 0.0

    # ------------------------
    # Find size.number_range anywhere in the payload (recursive search)
    # ------------------------
    def find_size_number_range_anywhere(obj: Any) -> Optional[tuple]:
        if isinstance(obj, dict):
            if "size" in obj and isinstance(obj["size"], dict):
                nr = obj["size"].get("number_range")
                if isinstance(nr, dict) and "minimum" in nr and "maximum" in nr:
                    try:
                        mn = int(str(nr["minimum"]))
                        mx = int(str(nr["maximum"]))
                        if mn <= mx:
                            return (mn, mx)
                    except Exception:
                        pass
            # search nested dicts
            for v in obj.values():
                r = find_size_number_range_anywhere(v)
                if r:
                    return r
        elif isinstance(obj, list):
            for item in obj:
                r = find_size_number_range_anywhere(item)
                if r:
                    return r
        return None

    # ------------------------
    # Build 5-sqm intervals strictly from the given min..max
    # ------------------------
    def build_5sqm_intervals(min_sqm: int, max_sqm: int, step: int = 5) -> List[tuple]:
        intervals = []
        current = min_sqm
        while current <= max_sqm:
            hi = current + (step - 1)
            if hi > max_sqm:
                hi = max_sqm
            intervals.append((current, hi))
            current = hi + 1
        return intervals

    # ------------------------
    # Try to inject size filters into a copy of the payload (prefer 'size.number_range' if possible)
    # ------------------------
    
    def try_set_size_filters(payload_in: dict, min_sqm: int, max_sqm: int) -> dict:
        # deep copy so the original payload is not modified
        p = json.loads(json.dumps(payload_in))
    
        try:
            # navigate to the correct nested 'data' dictionary
            data = p["search_data"]["form_data"]["data"]
    
            # ensure 'size' and 'number_range' exist
            if "size" not in data or not isinstance(data["size"], dict):
                data["size"] = {}
    
            if "number_range" not in data["size"] or not isinstance(data["size"]["number_range"], dict):
                data["size"]["number_range"] = {}
    
            # set the min/max values
            data["size"]["number_range"]["minimum"] = str(min_sqm)
            data["size"]["number_range"]["maximum"] = str(max_sqm)
    
        except Exception:
            # silently ignore if the structure is unexpected
            pass
    
        return p


    # ------------------------
    # Heuristics: extract posts and next cursor
    # ------------------------
    def extract_posts_from_response(resp_json: dict):
        posts_local = None
        for key in ("posts", "widget_list", "items", "data"):
            if isinstance(resp_json, dict) and isinstance(resp_json.get(key), list):
                posts_local = resp_json[key]
                break
        if posts_local is None:
            def find_first_list_of_dicts(obj):
                if isinstance(obj, list) and obj and isinstance(obj[0], dict):
                    return obj
                if isinstance(obj, dict):
                    for v in obj.values():
                        r = find_first_list_of_dicts(v)
                        if r:
                            return r
                return None
            posts_local = find_first_list_of_dicts(resp_json) or []
        return posts_local

    def find_next_cursor(resp_json: dict):
        if not isinstance(resp_json, dict):
            return None
        for k in ("next_cursor", "next", "cursor", "nextPage", "next_page", "continuation", "last_token"):
            v = resp_json.get(k)
            if v:
                if isinstance(v, dict):
                    for subk in ("cursor", "token", "last_token"):
                        if v.get(subk):
                            return v.get(subk)
                elif isinstance(v, (str, int)):
                    return v
        meta = resp_json.get("meta") or resp_json.get("paging") or resp_json.get("pagination")
        if isinstance(meta, dict):
            for k in ("next_cursor", "next", "cursor", "next_page", "nextPage"):
                if meta.get(k):
                    return meta.get(k)
        return None

    def fetch_for_payload_with_pagination(base_url: str, headers: dict, payload_in: dict, timeout=REQUEST_TIMEOUT):
        combined = []
        seen_ids = set()
        page_num = 1

        p = json.loads(json.dumps(payload_in))
        supports_page = any(k in p for k in ("page", "offset", "page_number", "page_num"))

        while True:
            if supports_page:
                if "page" in p:
                    p["page"] = page_num
                elif "page_number" in p:
                    p["page_number"] = page_num
                elif "page_num" in p:
                    p["page_num"] = page_num
                elif "offset" in p:
                    p["offset"] = (page_num - 1) * PAGE_SIZE_GUESS

            try:
                save_json(p, f"request_payload_debug_page{page_num}.json")
                resp = requests.post(base_url, headers=headers, json=p, timeout=timeout)
                resp.raise_for_status()
                data_local = resp.json()
            except Exception as e:
                print("Error fetching posts (pagination):", e)
                break

            posts_chunk = extract_posts_from_response(data_local) or []
            for post in posts_chunk:
                pid = post.get("id") or post.get("token") or post.get("post_token") or post.get("postId")
                if not pid:
                    pid = json.dumps(post, sort_keys=True, ensure_ascii=False)
                if pid not in seen_ids:
                    combined.append(post)
                    seen_ids.add(pid)

            if len(posts_chunk) < PAGE_SIZE_GUESS and not find_next_cursor(data_local):
                break

            cursor = find_next_cursor(data_local)
            if cursor:
                for ck in ("cursor", "next_cursor", "continuation", "last_token"):
                    p[ck] = cursor
                page_num += 1
                time.sleep(RATE_LIMIT_SLEEP)
                continue
            else:
                if supports_page:
                    page_num += 1
                    if not posts_chunk:
                        break
                    time.sleep(RATE_LIMIT_SLEEP)
                    continue
                break

        return combined

    # ------------------------
    # Determine requested min/max either from payload or default
    # ------------------------
    explicit = find_size_number_range_anywhere(payload)
    if explicit:
        min_requested, max_requested = explicit
    else:
        min_requested, max_requested = 75, 120

    # Build size ranges strictly from the requested interval
    size_ranges = build_5sqm_intervals(min_requested, max_requested, step=5)
    print(f"Using requested size range: {min_requested} - {max_requested}")
    print(f"Will request {len(size_ranges)} ranges: {size_ranges}")

    # ------------------------
    # Request each interval (server-side) and collect posts (deduped)
    # ------------------------
    all_posts_combined = []
    all_seen_ids = set()

    for (min_sqm, max_sqm) in size_ranges:
        print(f"Requesting server for size {min_sqm}-{max_sqm} ...")
        modified_payload = try_set_size_filters(payload, min_sqm, max_sqm)
        posts_for_range = fetch_for_payload_with_pagination(url, headers, modified_payload)
        time.sleep(0.02)

        for post in posts_for_range:
            pid = post.get("map_post_card").get("id") or post.get("map_post_card").get("token") or post.get("map_post_card").get("post_token") or post.get("map_post_card").get("postId")
            if not pid:
                pid = json.dumps(post, sort_keys=True, ensure_ascii=False)
            if pid not in all_seen_ids:
                all_posts_combined.append(post)
                all_seen_ids.add(pid)

        print(f"  fetched {len(posts_for_range)} posts for this range; cumulative unique posts: {len(all_posts_combined)}")
        time.sleep(RATE_LIMIT_SLEEP)

    # If nothing collected, fallback to a single paginated request
    if not all_posts_combined:
        print("No posts collected per-range. Falling back to a single paginated request without size filters.")
        fallback_posts = fetch_for_payload_with_pagination(url, headers, payload)
        for post in fallback_posts:
            pid = post.get("id") or post.get("token") or post.get("post_token") or post.get("postId")
            if not pid:
                pid = json.dumps(post, sort_keys=True, ensure_ascii=False)
            if pid not in all_seen_ids:
                all_posts_combined.append(post)
                all_seen_ids.add(pid)

    print(f"Collected total unique posts (before client-side filtering): {len(all_posts_combined)}")
    posts = all_posts_combined

    # Save raw posts for traceability
    posts_filename = save_json(posts, f"posts_collected_{ts}.json")
    print(f"Saved collected posts -> {out_dir / posts_filename}")

    # ------------------------
    # CLIENT-SIDE STRICT FILTERING:
    # Only keep posts whose parsed size is known and between min_requested..max_requested inclusive.
    # This ensures averages only use items actually within the requested range.
    # ------------------------
    filtered_posts: List[Dict[str, Any]] = []
    for post in posts:
        map_post = post.get("map_post_card", {}) or {}
        parsed_size = parse_size(map_post)
        # keep only if parsed_size exists and is within requested bounds
        if parsed_size is not None and (min_requested <= parsed_size <= max_requested):
            filtered_posts.append(post)
    print(f"After client-side size filtering (keeping only posts with parsed size in {min_requested}-{max_requested}): {len(filtered_posts)}")

    # Replace posts with filtered_posts for subsequent calculations
    posts = filtered_posts

    # ------------------------
    # The rest of your original parsing/summary logic, but operating on 'posts' which
    # now contains only items within the requested size range and have known parsed sizes.
    # ------------------------
    valid_prices = []
    age_intervals = {"0-4": [], "5-9": [], "10-14": [], "15-20": []}
    # Keep the same coarse size buckets for compatibility, but they will be computed from filtered posts.
    size_intervals = {"<80": [], "80-120": [], ">120": []}
    age_size_matrix = {age: {"<80": [], "80-120": [], ">120": []} for age in age_intervals}

    parsed_rows: List[Dict[str, Any]] = []

    for post in posts:
        map_post = post.get("map_post_card", {}) or {}
        item_id = map_post.get("id") or map_post.get("token")
        item_title = map_post.get("title")
        price_per_meter = None
        for field in map_post.get("price_fields", []):
            if "متری" in field.get("title", ""):
                price_per_meter = parse_price(field.get("value", ""))
                break
        age = parse_age(map_post.get("chips", []) or [])
        size = parse_size(map_post)

        parsed_rows.append({
            "id": item_id,
            "title": item_title,
            "price_per_sqm": price_per_meter,
            "age": age,
            "size": size,
        })

        if price_per_meter and PRICE_FLOOR <= price_per_meter <= PRICE_CEILING:
            valid_prices.append(price_per_meter)

            # age_key classification
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
                    if size <= 80:
                        age_size_matrix[age_key]["<80"].append(price_per_meter)
                    elif 80 < size < 120:
                        age_size_matrix[age_key]["80-120"].append(price_per_meter)
                    else:
                        age_size_matrix[age_key][">120"].append(price_per_meter)

            # size-only buckets
            if size is not None:
                if size <= 80:
                    size_intervals["<80"].append(price_per_meter)
                elif 80 < size < 120:
                    size_intervals["80-120"].append(price_per_meter)
                else:
                    size_intervals[">120"].append(price_per_meter)

    summary = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "requested_size_min": min_requested,
        "requested_size_max": max_requested,
        "total_posts": len(posts),
        "valid_for_averages": len(valid_prices),
        "overall_avg_price_per_sqm": int(avg(valid_prices)) if valid_prices else 0,
        "age_intervals": {k: {"avg": int(avg(v)) if v else 0, "count": len(v)} for k, v in age_intervals.items()},
        "size_intervals": {k: {"avg": int(avg(v)) if v else 0, "count": len(v)} for k, v in size_intervals.items()},
        "age_size_matrix": {k: {kk: {"avg": int(avg(vv)) if vv else 0, "count": len(vv)} for kk, vv in v.items()} for k, v in age_size_matrix.items()},
    }

    summary_filename = save_json(summary, f"summary_{ts}.json")

    # Print human-readable summary
    print("\n=== SUMMARY ===")
    print(f"Timestamp: {summary['timestamp']}")
    print(f"Requested size range: {min_requested} - {max_requested}")
    print(f"Total posts used (size known & in range): {summary['total_posts']}")
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

    # Optionally save parsed rows
    # rows_filename = f"rows_parsed_{ts}.json"
    # save_json(parsed_rows, rows_filename)

    return {
        "posts_file": out_dir / posts_filename,
        "summary_file": out_dir / summary_filename,
        "out_dir": out_dir
    }

# ------------------------
# Cleanup function for old posts and omitted items files
# ------------------------
def cleanup_old_posts_files(district_path: str, keep_days: int = POSTS_RETENTION_DAYS):
    """
    Delete posts_collected_*.json(.gz) and omitted_items_*.json(.gz) files older than keep_days for a specific district.
    Keeps summary_*.json.gz files as they are much smaller and needed for charts.
    Handles both .json and .json.gz file extensions for backward compatibility.
    """
    district_dir = Path(district_path)
    if not district_dir.exists():
        return
    
    cutoff_date = datetime.now() - timedelta(days=keep_days)
    deleted_files = []
    deleted_size = 0
    
    for timestamp_dir in district_dir.iterdir():
        if not timestamp_dir.is_dir():
            continue
        
        try:
            timestamp_str = timestamp_dir.name
            dir_datetime = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            
            if dir_datetime < cutoff_date:
                for ext in ("json.gz", "json"):
                    posts_file = timestamp_dir / f"posts_collected_{timestamp_str}.{ext}"
                    if posts_file.exists():
                        file_size = posts_file.stat().st_size
                        posts_file.unlink()
                        deleted_files.append(str(posts_file))
                        deleted_size += file_size
                        print(f"Deleted old posts file: {posts_file} ({file_size/1024/1024:.1f} MB)")
                    
                    omitted_file = timestamp_dir / f"omitted_items_{timestamp_str}.{ext}"
                    if omitted_file.exists():
                        file_size = omitted_file.stat().st_size
                        omitted_file.unlink()
                        deleted_files.append(str(omitted_file))
                        deleted_size += file_size
                        print(f"Deleted old omitted items file: {omitted_file} ({file_size/1024/1024:.1f} MB)")
                
                try:
                    timestamp_dir.rmdir()
                    print(f"Removed empty directory: {timestamp_dir}")
                except OSError:
                    pass
                        
        except (ValueError, FileNotFoundError):
            continue
    
    if deleted_files:
        print(f"Cleanup complete for {district_path}: deleted {len(deleted_files)} files, freed {deleted_size/1024/1024:.1f} MB")
    else:
        print(f"No old files to delete in {district_path}")


# ------------------------
