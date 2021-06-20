from urllib.request import urlopen, Request
from urllib.parse import urlencode, unquote, quote_plus 
import urllib, requests, json, datetime

def show_weather():
    # 초단기 실황 url
    url1 = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst'
    # 동네 예보 url
    url2 = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst'

    # key decode
    serviceKey = unquote('ncZFNuwHLlEgOaXOhrG6%2FAsT3v6h0fIZn4MjReMHQl8dBpuc1ObH0ZB6y%2BebHMjurHcN4tv02w5FkD7dFfuREw%3D%3D')

    # 시간 계산
    now_time = str(datetime.datetime.now())
    date = now_time.split()[0].replace("-", "")
    hour = int(now_time.split()[1][:2]) + 8 % 24
    minute = int(now_time.split()[1][3:5])

    # print(date, hour, minute)

    # 초단기 실황 호출 시간 계산
    short_term_hour = hour
    short_term_date = date
    if minute <= 40:
        short_term_hour = (short_term_hour - 1) % 24
        if short_term_hour == 23:
            short_term_date = short_term_date[:-2] + '{0:0>2}'.format(int(short_term_date[-2:]) - 1)
    short_term_base_time = "0" + str(short_term_hour) + "00" if short_term_hour < 10 else str(short_term_hour) + "00"
    # print(short_term_date, short_term_base_time)

    # 동네 예보 호출 시간 계산
    forecast_date = date
    call_time = int('{0:0>2}{1:0>2}'.format(hour,minute))
    # print(call_time)
    if 230 < call_time <= 530:
        forecast_base_time = '0200'
    elif 530 < call_time <= 830:
        forecast_base_time = '0500'
    elif 830 < call_time <= 1130:
        forecast_base_time = '0800'
    elif 1130 < call_time <= 1430:
        forecast_base_time = '1100'
    elif 1430 < call_time <= 1730:
        forecast_base_time = '1400'
    elif 1730 < call_time <= 2030:
        forecast_base_time = '1700'
    elif 2030 < call_time <= 2330:
        forecast_base_time = '2000'
    else:
        forecast_base_time = '2300'
        if call_time < 230:
            forecast_date = forecast_date[:-2] + '{0:0>2}'.format(int(forecast_date[-2:]) - 1)
    # print(forecast_date, forecast_base_time)


    # # 초단기 실황 request
    queryParams1 = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('pageNo') : '1', quote_plus('numOfRows') : '10', quote_plus('dataType') : 'json', quote_plus('base_date') : short_term_date, quote_plus('base_time') : short_term_base_time, quote_plus('nx') : 60, quote_plus('ny') : 121})
    request1 = urllib.request.Request(url1 + queryParams1)
    request1.get_method = lambda: 'GET'
    response_body = urlopen(request1).read()
    response_json_format1 = json.loads(response_body)

    # # 동네예보 request
    queryParams2 = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('pageNo') : '1', quote_plus('numOfRows') : '10', quote_plus('dataType') : 'json', quote_plus('base_date') : forecast_date, quote_plus('base_time') : forecast_base_time, quote_plus('nx') : 60, quote_plus('ny') : 121})
    request2 = urllib.request.Request(url2 + queryParams2)
    request2.get_method = lambda: 'GET'
    response_body = urlopen(request2).read()
    response_json_format2 = json.loads(response_body)

    # print(response_json_format1)
    format1_data_dict = response_json_format1['response']['body']['items']['item']
    format2_data_dict = response_json_format2['response']['body']['items']['item']
    # print(format1_data_dict)
    # print(format2_data_dict)
    
    #초단기 => 기온(T1H), 1시간강수량(RN1), 습도(REH), 강수형태(PTY)
    #동네예보 => 강수확률(POP), 하늘상태(SKY)
    #강수형태 => 없음(0), 비(1), 진눈깨비(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)
    #하늘상태(SKY) => 맑음(1), 구름많음(3), 흐림(4)
    temperature = float(format1_data_dict[3]['obsrValue'])
    hourly_precipitation = int(format1_data_dict[2]['obsrValue'])
    humidity = int(format1_data_dict[1]['obsrValue'])
    precipitation_type = int(format1_data_dict[0]['obsrValue'])
    precipitation_probability = int(format2_data_dict[0]['fcstValue'])
    sky_status = int(format2_data_dict[5]['fcstValue'])
    # print('기온: {}'.format(format1_data_dict[3]['obsrValue']), '1시간 강수량: {}'.format(format1_data_dict[2]['obsrValue']), '습도: {}'.format(format1_data_dict[1]['obsrValue']), '강수형태: {}'.format(format1_data_dict[0]['obsrValue']), '강수확률: {}'.format(format2_data_dict[0]['fcstValue']), '하늘상태: {}'.format(format2_data_dict[3]['fcstValue']), sep="\n")
    # print('기온: {}'.format(format1_data_dict[3]['category']), '1시간 강수량: {}'.format(format1_data_dict[2]['category']), '습도: {}'.format(format1_data_dict[1]['category']), '강수형태: {}'.format(format1_data_dict[0]['category']), '강수확률: {}'.format(format2_data_dict[0]['category']), '하늘상태: {}'.format(format2_data_dict[3]['category']), sep="\n")
    return [temperature, hourly_precipitation, humidity, precipitation_type, precipitation_probability, sky_status]

# show_weather()