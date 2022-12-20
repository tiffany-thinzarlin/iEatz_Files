api_key = "AIzaSyDuqGl-r_6EMdZbBgml5nYde373e2X8Rq8"

import requests
from urllib.parse import urlencode

class GoogleMapsClient(object):
    lat = None
    lng = None
    data_type = 'json'
    location_query = None
    api_key = None
    result_amount = 3

    def __init__(self, api_key=None, address_or_postal_code=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if api_key == None:
            raise Exception("API key is required")
        self.api_key = api_key
        self.location_query = address_or_postal_code
        if self.location_query == None:
            raise ValueError('Please enter a valid location.')
        self.extract_lat_lng()


            #print(self.extract_lat_lng("42906 Fairlee Dr, Lancaster, CA"))
            #print(self.search(self.extract_lat_lng("1600 Amphitheatre Parkway, Mountain View, CA")))

    def extract_lat_lng(self):
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
        params = {"address":self.location_query, "key": self.api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
        if r.status_code not in range(200, 299):
            return {}
        latlng = {}
        try:
            latlng = r.json()['results'][0]['geometry']['location']
        except:
            pass
        lat,lng = latlng.get("lat"), latlng.get("lng")
        self.lat = lat
        self.lng = lng
        #return lat, lng
        return


    def search(self, keyword="Food", radius = 5000):
        places_endpoint_2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params_2 = {
            "key": self.api_key,
            "location": f"{self.lat},{self.lng}",
            "radius": radius,
            "keyword": keyword
        }
        params_2_encoded = urlencode(params_2)
        places_url = f"{places_endpoint_2}?{params_2_encoded}"

        r = requests.get(places_url)
        if r.status_code not in range(200,299):
            return {}

        self.detail_list(r.json())
        return r.json()


    def detail(self, place_id, fields=["name", "rating", "formatted_phone_number", "formatted_address"]):
        detail_base_endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
        detail_params = {
        "place_id": f"{place_id}",
        "fields" : ",".join(fields),
        "key": self.api_key
        }

        detail_params_encoded = urlencode(detail_params)

        detail_url = f"{detail_base_endpoint}?{detail_params_encoded}"

        r = requests.get(detail_url)
        if r.status_code not in range(200, 299):
            return {}

        print(r.json()['result']['name'])
        print(r.json()['result']['formatted_address'])
        print(r.json()['result']['rating'])
        print(r.json()['result']['formatted_phone_number'])

        #return r.json()

    def detail_list(self, json_list):
        for i in range(self.result_amount):
            place_id = json_list['results'][i]['place_id']
            self.detail(place_id)


# print(extract_lat_lng("42906 Fairlee Dr, Lancaster, CA"))
# print(search(extract_lat_lng("1600 Amphitheatre Parkway, Mountain View, CA")))
def main():
    gmc = GoogleMapsClient(api_key, "42906 Fairlee Dr, Lancaster, CA" )
    gmc.search("Chinese Food", radius = 5000)
    #gmc.detail(search(extract_lat_lng("42906 Fairlee Dr, Lancaster, CA")))


if __name__ == '__main__':
    main()