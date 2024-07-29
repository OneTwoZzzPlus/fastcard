from db import balloons, BalloonAns
import requests


def sorted_balloons(lat, lon):
    """ Сортирует заправки по расстоянию по прямой """
    return sorted(
        balloons,
        key=lambda x: (((x.latitude - lat) ** 2 + (x.longitude - lon) ** 2) ** 0.5)
    )


async def route_2gis(lat1, lon1, lat2, lon2):
    print(f'Routing between {lat1}, {lon1} and {lat2}, {lon2}')
    API_KEY = 'f621ae59-f0ca-45df-87be-075a2a1244a3'
    url = f'http://routing.api.2gis.com/routing/7.0.0/global?key={API_KEY}'
    json = {
        "points": [
            {"type": "stop", "lat": lat1, "lon": lon1},
            {"type": "stop", "lat": lat2, "lon": lon2}
        ],
        "locale": "ru", "transport": "car", "route_mode": "fastest", "traffic_mode": "jam"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=json, headers=headers)

    # with open('re.json', 'a', encoding='windows-1251') as f:
    #     f.write(response.text)

    if response.ok:
        return response.json()
    else:
        return None


async def get_nearest_balloons(lat, lon, count):
    """
    Получение ближайших заправок
    :param lat: широта пользователя
    :param lon: долгота пользователя
    :param count: количество запрашиваемых заправок
    :return: Список из заправок
    """

    ret: list[BalloonUser] = []

    for balloon in sorted_balloons(lat, lon)[:count]:
        ball_json = await route_2gis(balloon.latitude, balloon.longitude, lat, lon)
        if ball_json is not None:
            try:
                b_distance = ball_json['result'][0]['total_distance']
                b_time = ball_json['result'][0]['ui_total_duration']
                ret.append(
                    BalloonAns(
                        balloon=balloon,
                        distance=b_distance,
                        time=b_time,
                        is_occupied=False,
                        is_long=False
                    )
                )
            except KeyError as e:
                print(e)
                ret.append(
                    BalloonAns(
                        balloon=balloon,
                        distance=0,
                        time='',
                        is_occupied=False,
                        is_long=True
                    )
                )
        else:
            print(ball_json)
            ret.append(
                BalloonAns(
                    balloon=balloon,
                    distance=0,
                    time='',
                    is_occupied=False,
                    is_long=True
                )
            )
    return sorted(ret, key=lambda x: x.distance if x.distance is not None else 10 ** 10)
