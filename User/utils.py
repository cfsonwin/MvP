import numpy as np

def get_centroid(loc_dic):
    latlog = []
    for key in loc_dic.keys():
        info = loc_dic[key]
        latlog.append([float(info.lat), float(info.lon)])
    loc_array = np.array(latlog)
    max_lat = max(loc_array[:, 0])
    min_lat = min(loc_array[:, 0])
    max_lon = max(loc_array[:, 1])
    min_lon = min(loc_array[:, 1])
    loc_range = max([max_lat - min_lat, max_lon - min_lon])
    zoom_index = 18
    while loc_range > (360 / (2**zoom_index)):
        zoom_index -= 1
    latlog = np.average(loc_array, axis=0)
    return latlog, zoom_index



if __name__ == '__main__':
    class info:
        def __init__(self, lat, lon):
            self.lat = lat
            self.lon = lon

    loc_list = [
        [12, 45],
        [16, 49],
        [13, 54]
    ]
    loc_array = np.array(loc_list)
    max_lat = max(loc_array[:, 0])
    min_lat = min(loc_array[:, 0])
    max_lon = max(loc_array[:, 1])
    min_lon = min(loc_array[:, 1])
    loc_range = max([max_lat - min_lat, max_lon - min_lon])
    loc_dic = {}
    zoom_index = 2
    print(np.average(loc_array, axis=0))
    print(360 / (2**zoom_index))
    for i in range(len(loc_list)):
        loc_dic[i] = info(loc_list[i][0], loc_list[i][1])
    print(min_lat, max_lat, min_lon, max_lon, loc_range)