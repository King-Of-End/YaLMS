def get_scaling(toponym):
    delta_long = str(abs(float(toponym['boundedBy']['Envelope']['lowerCorner'].split(" ")[0]) -
                         float(toponym['boundedBy']['Envelope']['upperCorner'].split(" ")[0])))
    delta_lat = str(abs(float(toponym['boundedBy']['Envelope']['lowerCorner'].split(" ")[1]) -
                        float(toponym['boundedBy']['Envelope']['upperCorner'].split(" ")[1])))
    return ",".join([delta_long, delta_lat])