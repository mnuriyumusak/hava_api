import json
import urllib2
import csv

API_KEY = "***"
BASE_URL_WHEATHER = "http://my.meteoblue.com/packages/basic-day_current?name=&"
BASE_URL_GOOGLE = "http://maps.google.com/maps/api/geocode/json?address="
TAKEN_LIST = ["time","pictocode","uvindex","temperature_max","temperature_min","felttemperature_max","felttemperature_min",
              "winddirection","precipitation_probability","rainspot","predictability_class","predictability","precipitation",
              "snowfraction","sealevelpressure_max","sealevelpressure_min","sealevelpressure_mean","windspeed_max",
              "windspeed_mean","windspeed_min","relativehumidity_max","relativehumidity_min","relativehumidity_mean"]


def find_lat_and_lng(city_name):
    # This  part takes lat lng from google's api
    response = urllib2.urlopen(BASE_URL_GOOGLE+city_name+"&sensor=false")
    json_data = json.load(response)

    lat = json_data["results"][0]["geometry"]["location"]["lat"]
    lng = json_data["results"][0]["geometry"]["location"]["lng"]

    return [lat,lng]


def convert_to_csv(json_data):
    path = open("list.txt", 'a+')
    csvwriter = csv.writer(path,delimiter=';',lineterminator = ';')

    for k in range(len(json_data[TAKEN_LIST[0]])):
        for t in TAKEN_LIST:
            if t == TAKEN_LIST[0]:
                csvwriter = csv.writer(path,delimiter=';',lineterminator = ';')
            csvwriter.writerow([json_data[t][k]])
            if t == TAKEN_LIST[len(TAKEN_LIST)-2]:
                csvwriter = csv.writer(path,delimiter=';',lineterminator = '\n')

    path.close()


def find_and_write(city_name):
    lat_lng_list = find_lat_and_lng(city_name)
    final_url = BASE_URL_WHEATHER + "lat="+str(lat_lng_list[0])+"&lon=" + str(lat_lng_list[1]) + "&tz=Europe_" + \
                city_name + "&apikey=" + API_KEY
    # this part takes whether info from server
    response = urllib2.urlopen(final_url)
    json_data = json.load(response)["data_day"]
    convert_to_csv(json_data)


find_and_write("Ankara")

