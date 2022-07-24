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


# def get_geo(ip):
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


class LineInfo:
    def __init__(self, lat, lon, lat_p, lon_p):
        self.lat = lat
        self.lon = lon
        self.lat_p = lat_p
        self.lon_p = lon_p


class Manus:
    def __init__(self, this_manu, manufacturer, parent_info):
        self.pm_id = manufacturer.id
        self.name = this_manu.m_name
        self.lat = this_manu.loc.split(',')[0]
        self.lon = this_manu.loc.split(',')[1]
        self.status = manufacturer.status
        self.modify_time = manufacturer.modify_time
        self.addtime = manufacturer.add_time
        if self.modify_time == self.addtime:
            self.change_st = 0
            self.change_msg = 'No Modification'
        else:
            self.change_st = 1
            self.change_msg = self.get_time_diff()
        self.description = manufacturer.modify_log
        self.parent_info = parent_info
        self.log_dic = self.get_modify_log()
        self.addr = self.get_addr(this_manu.addr)
        self.producing_period = manufacturer.producing_period
        self.m_status = self.status_transfer(manufacturer.m_status)
        self.m_right = self.right_transfer(manufacturer.access_right)

    def get_addr(self, addr):
        addr_arr = addr.split(',')
        if len(addr_arr) >= 4:
            addr_newarr = addr.split(',')[-4:]
            addr = '%s,%s,%s,%s' % (
                addr_newarr[0],
                addr_newarr[1],
                addr_newarr[2],
                addr_newarr[3],
            )

        else:
            addr = addr
        return addr

    def right_transfer(self, m_right):
        return_list = ['---', '--x', '-w-', '-wx', 'r--', 'r-x', 'rw-', 'rwx']
        return return_list[int(m_right)]

    def status_transfer(self, m_status):
        return_list = ['Preparing', 'Manufacturing', 'Distributing']
        return return_list[int(m_status)]

    def get_modify_log(self):
        log = self.description
        log_dic = {}
        i = 0
        if ';;;' in log:
            while log.split(';;;')[i] != '':
                log_dic[log.split(';;;')[i].split('::')[0]] = log.split(';;;')[i].split('::')[1]
                i += 1
        else:
            log_dic['error'] = log
        return log_dic

    def get_time_diff(self):
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modifytime = self.modify_time.strftime("%Y-%m-%d %H:%M:%S")
        year_diff = int(time_now.split(' ')[0].split('-')[0]) - int(modifytime.split(' ')[0].split('-')[0])
        month_diff = int(time_now.split(' ')[0].split('-')[1]) - int(modifytime.split(' ')[0].split('-')[1])
        day_diff = int(time_now.split(' ')[0].split('-')[2]) - int(modifytime.split(' ')[0].split('-')[2])
        hour_diff = int(time_now.split(' ')[1].split(':')[0]) - int(modifytime.split(' ')[1].split(':')[0])
        if year_diff > 1:
            msg = 'Last Modification: %d years ago' % year_diff
        elif year_diff == 1:
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


def get_search_id(name, time_now):
    new_str = name + time_now
    md5 = hashlib.md5()
    md5.update(new_str.encode('utf-8'))
    return md5.hexdigest()


if __name__ == '__main__':
    # for i in range(20):
    #     pw = 'manu1234'
    #     md5 = hashlib.md5()
    #     ran_n = random.randint(100000, 999999)
    #     print(ran_n)
    #     # ran_n = 613249
    #     new_pass = pw + str(ran_n)  # 'admin123'
    #     md5.update(new_pass.encode('utf-8'))
    #     print(md5.hexdigest())
    # i += 1
    print(get_search_id("vProduct_7", "2022-04-10 18:49:26"))
