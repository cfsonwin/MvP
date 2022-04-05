import hashlib
import random
from datetime import datetime

# from django.contrib.gis.geoip2 import GeoIP2


def pw_hash(pw):
    md5 = hashlib.md5()
    ran_n = random.randint(100000, 999999)
    new_pass = pw + str(ran_n)  # 'admin123'
    md5.update(new_pass.encode('utf-8'))
    print(md5.hexdigest())
    print(ran_n)


def pw_hash_salt(pw, salt):
    md5 = hashlib.md5()
    ran_n = salt
    new_pass = pw + str(ran_n)  # 'admin123'
    md5.update(new_pass.encode('utf-8'))
    return md5.hexdigest()


#def get_geo(ip):
#    g = GeoIP2()
#    country = g.country(ip)
#    city = g.city(ip)
#    lat, lon = g.lat_lon(ip)
#    return country, city, lat, lon


def get_center_coor(lat1=None, lon1=None, lat2=None, lon2=None):
    coor = [49.875624225327876, 8.63731024952363]
    if lat1 and lat2:
        coor = [(lat1 + lat2) / 2, (lon1 + lon2) / 2]
    return coor


def get_zoom(distance):
    if distance <= 100:
        return 8
    elif distance > 100 and distance <= 5000:
        return 4
    else:
        return 2


class Manus:
    def __init__(self, name, loc, addtime, modify_time, description, parent_info):
        self.name = name
        self.lat = loc.split(',')[0]
        self.lon = loc.split(',')[1]
        self.modify_time = modify_time
        self.addtime = addtime
        if self.modify_time == self.addtime:
            self.change_st = 0
            self.change_msg = 'No Modification'
        else:
            self.change_st = 1
            self.change_msg = self.get_time_diff()
        self.description = description
        self.parent_info = parent_info

    def get_time_diff(self):
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modifytime = self.modify_time.strftime("%Y-%m-%d %H:%M:%S")
        # print(modifytime.split(' ')[0].split('-')[0])
        year_diff = int(time_now.split(' ')[0].split('-')[0]) - int(modifytime.split(' ')[0].split('-')[0])
        month_diff = int(time_now.split(' ')[0].split('-')[1]) - int(modifytime.split(' ')[0].split('-')[1])
        day_diff = int(time_now.split(' ')[0].split('-')[2]) - int(modifytime.split(' ')[0].split('-')[2])
        hour_diff = int(time_now.split(' ')[1].split(':')[0]) - int(modifytime.split(' ')[1].split(':')[0])
        # min_diff = int(time_now.split(' ')[1].split(':')[1]) - int(modifytime.split(' ')[1].split(':')[1])
        # sec_diff = int(time_now.split(' ')[1].split(':')[2]) - int(modifytime.split(' ')[1].split(':')[2])
        if year_diff > 1:
            msg = 'Last Modification: %d years ago' % year_diff
        elif year_diff ==1:
            month_count = year_diff * 12 + month_diff
            msg = 'Last Modification: %d month ago' % month_count
        else:
            if month_diff >= 1:
                msg = 'Last Modification: %d month ago' % month_diff
            else:
                if day_diff > 1:
                    msg = 'Last Modification: %d days ago' % day_diff
                elif day_diff == 1:
                    hour_count = day_diff * 24 + hour_diff
                    msg = 'Last Modification: %d hours ago' % hour_count
                else:
                    msg = 'Last Modification: today'

        return msg
