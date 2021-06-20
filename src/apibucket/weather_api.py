from . import oxford
from . import weather

def weather_control_update():
    # [temperature, hourly_precipitation, humidity, precipitation_type, precipitation_probability, sky_status]
    # 강수형태 => 없음(0), 비(1), 진눈깨비(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)
    # 하늘상태(SKY) => 맑음(1), 구름많음(3), 흐림(4)

    weather_information = weather.show_weather()
    print("기온 : {}, 시간당 강수량 : {}, 습도: {}, 강수 형태: {}, 강수 확률: {}, 하늘 상태: {}".format(*weather_information))

    temperature, hourly_precipitation, humidity, precipitation_type, precipitation_probability, sky_status = weather_information
    response_text = ""
    # 날씨가 맑다면
    if sky_status == 1:
        # 온도가 적당하면
        if temperature <= 28:
            response_text = "It's sunny"
            # 습하면
            if (humidity >= 40 and temperature >= 24) or (humidity >= 50 and (21 <= temperature <= 23)) or (humidity >= 60 and (18 <= temperature <= 20)) or (humidity >= 70):
                response_text += " but humid"
        # 온도가 높으면
        else:
            response_text = "It's too hot"
            # 습하면
            if (humidity >= 40 and temperature >= 24) or (humidity >= 50 and (21 <= temperature <= 23)) or (humidity >= 60 and (18 <= temperature <= 20)) or (humidity >= 70):
                response_text += " and humid"
        response_text += ". Current temperature is {} and humidity is {}%".format(temperature, humidity)
    # 구름이 많거나(mostly cloudy), 흐린(cloudy)데 비가 안오는 경우
    elif sky_status == 3 or (sky_status == 4 and precipitation_type == 0):
        response_text = "It's cloudy"
        if precipitation_probability >= 60:
            response_text += ". It looks like it's going to rain soon. The precipitation_probability is {}".format(precipitation_probability)
    else:
        response_text = "It's rainy. The hourly precipitation is {}".format(hourly_precipitation)
    print(response_text)
    return response_text

if __name__ == '__main__':
    weather_control_update()