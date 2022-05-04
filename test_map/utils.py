if __name__ == '__main__':
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="get_location")
    latitude = 49.861252
    longitude = 8.682602
    location = geolocator.reverse((49.861252,8.682602))
    addr = location.address
    addr = 'a,s,d,f,g'
    addr_arr = addr.split(',')
    if len(addr_arr) >= 4:
        addr_newarr = addr.split(',')[-4:]
        addr = '%s,%s,%s,%s' %(
            addr_newarr[0],
            addr_newarr[1],
            addr_newarr[2],
            addr_newarr[3],
        )

    else:
        addr = addr
    print(addr)