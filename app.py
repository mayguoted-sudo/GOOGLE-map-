import requests

# 注意：這裡需要填入你申請的 Google Maps API Key
API_KEY = "你的_GOOGLE_MAPS_API_KEY"

def get_location_coordinates(place_name):
    """
    步驟 1: 透過文字搜尋找到目的地的經緯度
    """
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": place_name,
        "inputtype": "textquery",
        "fields": "formatted_address,name,geometry",
        "key": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['status'] == 'OK' and data['candidates']:
        candidate = data['candidates'][0]
        location = candidate['geometry']['location']
        print(f"已找到目的地：{candidate['name']}")
        print(f"地址：{candidate['formatted_address']}")
        return location['lat'], location['lng']
    else:
        print("找不到該目的地！")
        return None, None

def search_nearby_facilities(lat, lng, facility_type, radius=500):
    """
    步驟 2: 根據經緯度搜尋附近的設施
    radius: 搜尋半徑 (公尺)
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": facility_type, # 例如：停車場
        "language": "zh-TW",      # 設定語言為繁體中文
        "key": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    if data['status'] == 'OK':
        print(f"\n--- 在附近 {radius} 公尺內找到以下 {facility_type} ---")
        for place in data['results']:
            name = place.get('name')
            rating = place.get('rating', '無評分')
            addr = place.get('vicinity') # 簡易地址
            
            print(f"店名: {name} | 評分: {rating} | 地址: {addr}")
            results.append(name)
    else:
        print("附近找不到相關設施。")
        
    return results

# 主程式流程
def main():
    if API_KEY == "你的_GOOGLE_MAPS_API_KEY":
        print("錯誤：請先填入你的 Google Maps API Key 才能執行此程式！")
        return

    dest = input("請輸入目的地 (例如：台北車站): ")
    facility = input("請輸入附近的設施 (例如：便利商店): ")
    
    # 1. 找地點經緯度
    lat, lng = get_location_coordinates(dest)
    
    # 2. 如果有找到地點，才找附近的設施
    if lat and lng:
        search_nearby_facilities(lat, lng, facility)

if __name__ == "__main__":
    main()