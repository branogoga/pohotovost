import urllib2
import urllib
import json
import sys
# import ipdb
from bs4 import BeautifulSoup


def read_url(url):
    data = urllib2.urlopen(url).read()
    soup = BeautifulSoup(data, "html.parser")

    address = u"{} {}".format(soup.find("span", { "itemprop" : "streetAddress" }).text, soup.find("span", { "itemprop" : "addressLocality" }).text)
    geourl = "https://maps.googleapis.com/maps/api/geocode/json"
    params = urllib.urlencode({"address":address.encode('utf-8',errors='replace'), "key": "AIzaSyBSvG2HflFKGGYvtu1hJzPgLbKxriyIb7s"})
    georesult = urllib2.urlopen("{}?{}".format(geourl, params)).read()
    georesult = json.loads(georesult)
    loc = georesult['results'][0]['geometry']['location']


    result = {
        "name": soup.find("span", { "class" : "name" }).text,
        "address": address,
        "lat": loc['lat'],
        'lon': loc['lng'],
        "phone": soup.find("span", { "itemprop" : "telephone" }).text,
    }  

    if soup.find("span", { "itemprop" : "addressLocality" }).text == u"Bratislava":
        return result
    # result = {
    #         "name": soup.find("span", { "class" : "name" }).text.encode('utf-8',errors='replace'),
    #         "adress": soup.find("span", { "itemprop" : "streetAddress" }).text.encode('utf-8',errors='replace'),
    #         "postcode": soup.find("span", { "itemprop" : "postalCode" }).text.encode('utf-8',errors='replace'),
    #         "city": soup.find("span", { "itemprop" : "addressLocality" }).text.encode('utf-8',errors='replace'),
    #         "phone": soup.find("span", { "itemprop" : "telephone" }).text.encode('utf-8',errors='replace'),
    #         "loc": loc,
    #         "openings": {
    #             "1": {
    #                 "open": "08:00",
    #                 "close": "24:00"
    #             },
    #             "2": {
    #                 "open": "08:00",
    #                 "close": "24:00"
    #             },
    #             "3": {
    #                 "open": "08:00",
    #                 "close": "24:00"
    #             },
    #             "4": {
    #                 "open": "08:00",
    #                 "close": "24:00"
    #             },
    #             "5": {
    #                 "open": "08:00",
    #                 "close": "24:00"
    #             },
    #             "6": {
    #                 "open": "08:00",
    #                 "close": "24:00"
    #             },
    #             "7": {
    #                 "open": "08:00",
    #                 "close": "24:00"
    #             }

    #         }
    #     }
    return result

results = []


url = sys.argv[1]
filename = sys.argv[2]

data = urllib2.urlopen(url).read()
basesoup = BeautifulSoup(data, "html.parser")


for i in basesoup.findAll('a'):
    if i.parent.name == 'h2':
        baseurl = "https://www.zzz.sk{}".format(i['href'])
        
        try:
            result = read_url(baseurl)
            results.append(result)
        except:
            pass

# f = open(filename, 'w+')
# f.write(json.dumps(results))

print json.dumps(results)

