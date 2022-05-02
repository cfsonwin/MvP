import numpy as np
from Admin.utils import Manus, LineInfo

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
    while loc_range > (360 / (2 ** zoom_index)):
        zoom_index -= 1
    latlog = np.average(loc_array, axis=0)
    return latlog, zoom_index





