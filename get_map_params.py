def get_maps_params(json_response):
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    delta_long = str(abs(float(toponym['boundedBy']['Envelope']['lowerCorner'].split(" ")[0]) -
                         float(toponym['boundedBy']['Envelope']['upperCorner'].split(" ")[0])))
    delta_lat = str(abs(float(toponym['boundedBy']['Envelope']['lowerCorner'].split(" ")[1]) -
                        float(toponym['boundedBy']['Envelope']['upperCorner'].split(" ")[1])))
    org_point = f"{toponym_longitude},{toponym_lattitude}"

    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta_long, delta_lat]),
        "apikey": apikey,
        'pt': "{0},pm2dgl".format(org_point)
    }

    return map_params
