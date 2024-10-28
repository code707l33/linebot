import requests
import json
from datetime import datetime


def get_weather_city(city_name=''):

    city_name = city_name.replace('台', '臺')

    apikey = 'CWA-65283F2A-5A45-4772-8C57-9650A2A40C9E'
    dataid = ''
    url = f'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/{dataid}?Authorization={apikey}&format=json'

    furl = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-65283F2A-5A45-4772-8C57-9650A2A40C9E&format=JSON'

    r = requests.get(furl)

    if r.status_code == 200:
        data = r.json()

    locations = data['records']['location']

    output_dict = {}

    # Wx(天氣現象)、MaxT(最高溫度)、MinT(最低溫度)、CI(舒適度)、PoP(降雨機率)
    for location in locations:
        city = location['locationName']  # location
        for weather in location['weatherElement']:
            if weather['elementName'] == 'Wx':
                # 天氣日
                weather_element_day = weather['time'][0]['parameter']['parameterName']
                # 天氣夜
                weather_element_night = weather['time'][1]['parameter']['parameterName']
            elif weather['elementName'] == 'MaxT':
                # 最高溫度日
                max_t_day = weather['time'][0]['parameter']['parameterName']
                # 最高溫度夜
                max_t_night = weather['time'][1]['parameter']['parameterName']
            elif weather['elementName'] == 'MinT':
                # 最低溫度日
                min_t_day = weather['time'][0]['parameter']['parameterName']
                # 最低溫度夜
                min_t_night = weather['time'][1]['parameter']['parameterName']
            elif weather['elementName'] == 'CI':
                # 舒適度日
                ci_day = weather['time'][0]['parameter']['parameterName']
                # 舒適度夜
                ci_night = weather['time'][1]['parameter']['parameterName']
            elif weather['elementName'] == 'PoP':
                # 降雨機率日
                po_p_day = weather['time'][0]['parameter']['parameterName']
                # 降雨機率夜
                po_p_night = weather['time'][1]['parameter']['parameterName']
        # print(f'今日 {city} 天氣:\n日間\t{weather_element_day}\n\t最高溫度:{max_t_day}\t最低溫度:{min_t_day}\n\t舒適度:{ci_day}\n\t降雨機率:{po_p_day}%\n夜間\t{weather_element_night}\n\t最高溫度:{max_t_night}\t最低溫度:{min_t_night}\n\t舒適度:{ci_night}\n\t降雨機率:{po_p_night}%')
        msg = (f'今日 {city} 天氣:\n日間\t{weather_element_day}\n\t最高溫度:{max_t_day}\t最低溫度:{min_t_day}\n\t舒適度:{ci_day}\n\t降雨機率:{po_p_day}%\n夜間\t{weather_element_night}\n\t最高溫度:{max_t_night}\t最低溫度:{min_t_night}\n\t舒適度:{ci_night}\n\t降雨機率:{po_p_night}%')
        output_dict[city] = msg

    for city in output_dict.keys():
        if city_name in city:
            city_name = city
            break

    try:
        if city_name == '':
            return output_dict
        else:
            return output_dict[city_name]
    except Exception as e:
        err_msg = {'error': '查無此地區'}
        return err_msg


if __name__ == '__main__':
    print(get_weather_city('台北'))
