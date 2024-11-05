# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
import time
import random

apikey = 'CWA-65283F2A-5A45-4772-8C57-9650A2A40C9E'


def generate_color():

    rgb_list = []

    for i in range(20):
        # 隨機生成兩個高亮度通道
        high_values = [random.randint(180, 210) for _ in range(2)]
        # 隨機生成一個較低亮度通道，來增加彩度
        low_value = random.randint(100, 150)

        # 將兩個高亮值和一個低亮值合併成 RGB 列表
        rgb = high_values + [low_value]
        # 隨機打亂 RGB 列表的順序，以隨機排列 R, G, B 的值
        random.shuffle(rgb)

        rgb_list.append(rgb)

    # 解構列表，分別賦值給 r, g, b
    r, g, b = rgb_list[random.randint(0, 19)]

    # 如果顏色接近黃色，進一步降低藍色值來增加飽和度
    if r > 200 and g > 200 and b < 100:
        b = max(0, b - 50)  # 降低藍色值，但不低於 0

    # 將 r, g, b 格式化為 16 進制字串，並回傳
    return f"#{r:02x}{g:02x}{b:02x}"


def city_name_format(city_name):
    city_name = city_name.replace('台', '臺')

    city_full_name_list = ['宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣', '臺北市', '新北市', '桃園市',
                           '臺中市', '臺南市', '高雄市', '基隆市', '新竹縣', '新竹市', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '嘉義市', '屏東縣']

    for city_full_name in city_full_name_list:
        if city_name in city_full_name:
            city_name = city_full_name

    return city_name


def format_location(input_location):

    if input_location == '':
        return None
    locations = {
        '新北市': ['板橋區', '三重區', '中和區', '永和區', '新莊區', '新店區', '樹林區', '鶯歌區', '三峽區', '淡水區', '汐止區', '瑞芳區', '土城區', '蘆洲區', '五股區', '泰山區', '林口區', '深坑區', '石碇區', '坪林區', '三芝區', '石門區', '八里區', '平溪區', '雙溪區', '貢寮區', '金山區', '萬里區', '烏來區'],
        '臺北市': ['松山區', '信義區', '大安區', '中山區', '中正區', '大同區', '萬華區', '文山區', '南港區', '內湖區', '士林區', '北投區'],
        '桃園市': ['桃園區', '中壢區', '大溪區', '楊梅區', '蘆竹區', '大園區', '龜山區', '八德區', '龍潭區', '平鎮區', '新屋區', '觀音區', '復興區'],
        '臺中市': ['中區', '東區', '南區', '西區', '北區', '西屯區', '南屯區', '北屯區', '豐原區', '東勢區', '大甲區', '清水區', '沙鹿區', '梧棲區', '后里區', '神岡區', '潭子區', '大雅區', '新社區', '石岡區', '外埔區', '大安區', '烏日區', '大肚區', '龍井區', '霧峰區', '太平區', '大里區', '和平區'],
        '臺南市': ['新營區', '鹽水區', '白河區', '柳營區', '後壁區', '東山區', '麻豆區', '下營區', '六甲區', '官田區', '大內區', '佳里區', '學甲區', '西港區', '七股區', '將軍區', '北門區', '新化區', '善化區', '新市區', '安定區', '山上區', '玉井區', '楠西區', '南化區', '左鎮區', '仁德區', '歸仁區', '關廟區', '龍崎區', '永康區', '東區', '南區', '北區', '安南區', '安平區', '中西區'],
        '宜蘭縣': ['宜蘭市', '羅東鎮', '蘇澳鎮', '頭城鎮', '礁溪鄉', '壯圍鄉', '員山鄉', '冬山鄉', '五結鄉', '三星鄉', '大同鄉', '南澳鄉'],
        '新竹縣': ['竹北市', '關西鎮', '新埔鎮', '竹東鎮', '湖口鄉', '橫山鄉', '新豐鄉', '芎林鄉', '寶山鄉', '北埔鄉', '峨眉鄉', '尖石鄉', '五峰鄉'],
        '苗栗縣': ['苗栗市', '頭份市', '苑裡鎮', '通霄鎮', '竹南鎮', '後龍鎮', '卓蘭鎮', '大湖鄉', '公館鄉', '銅鑼鄉', '南庄鄉', '頭屋鄉', '三義鄉', '西湖鄉', '造橋鄉', '三灣鄉', '獅潭鄉', '泰安鄉'],
        '彰化縣': ['彰化市', '員林市', '鹿港鎮', '和美鎮', '北斗鎮', '溪湖鎮', '田中鎮', '二林鎮', '線西鄉', '伸港鄉', '福興鄉', '秀水鄉', '花壇鄉', '芬園鄉', '大村鄉', '埔鹽鄉', '埔心鄉', '永靖鄉', '社頭鄉', '二水鄉', '田尾鄉', '埤頭鄉', '芳苑鄉', '大城鄉', '竹塘鄉', '溪州鄉'],
        '南投縣': ['南投市', '埔里鎮', '草屯鎮', '竹山鎮', '集集鎮', '名間鄉', '鹿谷鄉', '中寮鄉', '魚池鄉', '國姓鄉', '水里鄉', '信義鄉', '仁愛鄉'],
        '雲林縣': ['斗六市', '斗南鎮', '虎尾鎮', '西螺鎮', '土庫鎮', '北港鎮', '古坑鄉', '大埤鄉', '莿桐鄉', '林內鄉', '二崙鄉', '崙背鄉', '麥寮鄉', '東勢鄉', '褒忠鄉', '臺西鄉', '元長鄉', '四湖鄉', '口湖鄉', '水林鄉'],
        '嘉義縣': ['太保市', '朴子市', '布袋鎮', '大林鎮', '民雄鄉', '溪口鄉', '新港鄉', '六腳鄉', '東石鄉', '義竹鄉', '鹿草鄉', '水上鄉', '中埔鄉', '竹崎鄉', '梅山鄉', '番路鄉', '大埔鄉', '阿里山鄉'],
        '屏東縣': ['屏東市', '潮州鎮', '東港鎮', '恆春鎮', '萬丹鄉', '長治鄉', '麟洛鄉', '九如鄉', '里港鄉', '鹽埔鄉', '高樹鄉', '萬巒鄉', '內埔鄉', '竹田鄉', '新埤鄉', '枋寮鄉', '新園鄉', '崁頂鄉', '林邊鄉', '南州鄉', '佳冬鄉', '琉球鄉', '車城鄉', '滿州鄉', '枋山鄉', '三地門鄉', '霧臺鄉', '瑪家鄉', '泰武鄉', '來義鄉', '春日鄉', '獅子鄉', '牡丹鄉'],
        '臺東縣': ['臺東市', '成功鎮', '關山鎮', '卑南鄉', '大武鄉', '太麻里鄉', '東河鄉', '長濱鄉', '鹿野鄉', '池上鄉', '綠島鄉', '延平鄉', '海端鄉', '達仁鄉', '金峰鄉', '蘭嶼鄉'],
        '花蓮縣': ['花蓮市', '鳳林鎮', '玉里鎮', '新城鄉', '吉安鄉', '壽豐鄉', '光復鄉', '豐濱鄉', '瑞穗鄉', '富里鄉', '秀林鄉', '卓溪鄉'],
        '澎湖縣': ['馬公市', '湖西鄉', '白沙鄉', '西嶼鄉', '望安鄉', '七美鄉'],
        '金門縣': ['金沙鎮', '金湖鎮', '金寧鄉', '金城鎮', '烈嶼鄉', '烏坵鄉'],
        '高雄市': ['鹽埕區', '鼓山區', '左營區', '楠梓區', '三民區', '新興區', '前金區', '苓雅區', '前鎮區', '旗津區', '小港區', '鳳山區', '林園區', '大寮區', '大樹區', '大社區', '仁武區', '鳥松區', '岡山區', '橋頭區', '燕巢區', '田寮區', '阿蓮區', '路竹區', '湖內區', '茄萣區', '永安區', '彌陀區', '梓官區', '旗山區', '美濃區', '六龜區', '甲仙區', '杉林區', '內門區', '茂林區', '桃源區', '那瑪夏區'],
        '連江縣': ['南竿鄉', '北竿鄉', '莒光鄉', '東引鄉']
    }
    # 標準化輸入，移除空白並轉成正體中文
    normalized_input = input_location.strip()
    normalized_input = normalized_input.replace("台", "臺")
    # 遍歷 locations 字典以查找匹配的城市和區域
    for city, districts in locations.items():
        # 若輸入包含完整的城市名稱
        if normalized_input in city:
            for district in districts:
                if district in normalized_input:
                    return f"{city}{district}"
            return [city]

        # 若輸入僅為區域名稱或是城市+區域的簡寫
        for district in districts:
            if normalized_input in district:
                return [city, district]

            # 針對 "城市+區域" 的不同簡寫格式進行檢查
            replacements = ["市區", "市鄉", "市鎮", "縣市", "縣區", "縣鄉", "縣鎮"]
            for rep in replacements:
                if normalized_input == city.replace(rep[:1], "") + district.replace(rep[1:], ""):
                    return [city, district]

    return None


def get_dataid(city_name):

    apidict = {'宜蘭縣': '/v1/rest/datastore/F-D0047-003', '桃園市': '/v1/rest/datastore/F-D0047-007', '新竹縣': '/v1/rest/datastore/F-D0047-011', '苗栗縣': '/v1/rest/datastore/F-D0047-015', '彰化縣': '/v1/rest/datastore/F-D0047-019', '南投縣': '/v1/rest/datastore/F-D0047-023', '雲林縣': '/v1/rest/datastore/F-D0047-027', '嘉義縣': '/v1/rest/datastore/F-D0047-031', '屏東縣': '/v1/rest/datastore/F-D0047-035', '臺東縣': '/v1/rest/datastore/F-D0047-039', '花蓮縣': '/v1/rest/datastore/F-D0047-043',
               '澎湖縣': '/v1/rest/datastore/F-D0047-047', '基隆市': '/v1/rest/datastore/F-D0047-051', '新竹市': '/v1/rest/datastore/F-D0047-055', '嘉義市': '/v1/rest/datastore/F-D0047-059', '臺北市': '/v1/rest/datastore/F-D0047-063', '高雄市': '/v1/rest/datastore/F-D0047-067', '新北市': '/v1/rest/datastore/F-D0047-071', '臺中市': '/v1/rest/datastore/F-D0047-075', '臺南市': '/v1/rest/datastore/F-D0047-079', '連江縣': '/v1/rest/datastore/F-D0047-083', '金門縣': '/v1/rest/datastore/F-D0047-087'}
    return apidict[city_name_format(city_name)]


def get_weather_city(city_name):

    # furl = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={apikey}&locationName=%E8%8A%B1%E8%93%AE%E7%B8%A3&format=JSON'
    furl = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-65283F2A-5A45-4772-8C57-9650A2A40C9E&format=JSON&locationName={city_name}'

    r = requests.get(furl)

    if r.status_code == 200:
        data = r.json()

    weatherElement = data['records']['location'][0]['weatherElement']

    # print(weatherElement[0])

    Wx = weatherElement[0]['time']
    Pop = weatherElement[1]['time']

    dic = {
        "type": "carousel",
        "contents": []
    }
    for z in zip(Wx, Pop):
        st = z[0]['startTime']
        Wx_value = z[0]['parameter']['parameterName']
        Pop_value = z[1]['parameter']['parameterName']

        # 解析原始字串為 datetime 對象
        dt = datetime.strptime(st, "%Y-%m-%d %H:%M:%S")

        # 格式化 datetime 為指定格式
        st = dt.strftime("%m月%d日 %I %p")
        dic['contents'].append({"type": "bubble", "size": "micro", "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": f"{city_name[:-1]}", "color": "#ffffff", "align": "start", "size": "20px", "gravity": "center"}, {"type": "text", "text": st, "color": "#ffffff", "align": "start", "size": "xs", "gravity": "center", "margin": "lg"}], "backgroundColor": generate_color(), "spacing": "sm", "paddingTop": "19px",
                               "paddingAll": "12px", "paddingBottom": "16px"}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": Wx_value, "size": "18px"}, {"type": "text", "text": f"降雨機率{Pop_value}%", "size": "15px"}, {"type": "box", "layout": "vertical", "contents": [], "backgroundColor": "#0D8186", "width": f"{Pop_value}%", "height": "6px"}], "spacing": "md", "paddingAll": "12px"}, "styles": {"footer": {"separator": False}}})

    return (dic)


def get_weather_dict(city_name, dist_name):

    dataid = get_dataid(city_name)
    url = f'https://opendata.cwa.gov.tw/api/{dataid}?Authorization={apikey}&format=JSON&locationName={dist_name}'
    print(url)
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
    else:
        return ('Error')

    # 取得天氣資訊、降雨機率
    weatherElements = data['records']['locations'][0]['location'][0]['weatherElement']
    Pop = weatherElements[0]['time'][:4]
    Wx = weatherElements[6]['time'][:4]

    dic = {
        "type": "carousel",
        "contents": []
    }
    for z in zip(Wx, Pop):
        st = z[0]['startTime']
        Wx_value = z[0]['elementValue'][0]['value']
        Pop_value = z[1]['elementValue'][0]['value']

        # 解析原始字串為 datetime 對象
        dt = datetime.strptime(st, "%Y-%m-%d %H:%M:%S")

        # 格式化 datetime 為指定格式
        st = dt.strftime("%m月%d日 %I %p")
        dic['contents'].append({"type": "bubble", "size": "micro", "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": f"{city_name[:-1]},{dist_name[:-1]}", "color": "#ffffff", "align": "start", "size": "20px", "gravity": "center"}, {"type": "text", "text": st, "color": "#ffffff", "align": "start", "size": "xs", "gravity": "center", "margin": "lg"}], "backgroundColor": generate_color(), "paddingTop": "19px",
                               "paddingAll": "12px", "paddingBottom": "16px"}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": Wx_value, "size": "18px"}, {"type": "text", "text": f"降雨機率{Pop_value}%", "size": "15px"}, {"type": "box", "layout": "vertical", "contents": [], "backgroundColor": "#0D8186", "width": f"{Pop_value}%", "height": "6px"}], "spacing": "md", "paddingAll": "12px"}, "styles": {"footer": {"separator": False}}})

    return (dic)


def get_weather(place):

    place = place.replace('天氣', '')
    place = place.replace(' ', '')

    dist = format_location(place)
    # print(dist)
    if dist is not None:
        if len(dist) == 1:
            return (get_weather_city(dist[0]))
        else:
            return (get_weather_dict(dist[0], dist[1]))
    else:
        return (None)


if __name__ == '__main__':

    print(type(get_weather('台北市')))
