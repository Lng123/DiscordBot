import requests
import json
import os


class Yelp:
    def __init__(self):
        self.api_key = os.environ["YELP_API_TOKEN"]
        self.headers = {'Authorization': 'Bearer %s' % self.api_key}

    def business_search(self):
        url = "https://api.yelp.com/v3/businesses/search"
        params = {'term': 'seafood', 'location': 'Vancouver, BC'}
        req = requests.get(url, params=params,
                           headers=self.headers)
        print('The status code is {}'.format(req.status_code))

        return json.loads(req.text)

    def id_search(self, id):
        url = f"https://api.yelp.com/v3/businesses/{id}"
        req = requests.get(url, headers=self.headers)
        print('The status code is {}'.format(req.status_code))

        return json.loads(req.text)

    def jprint(self, obj):
        """
        Create and print a formatted string of the Python JSON object
        """
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def get_info(self, request):
        info = []
        businesses = request["businesses"]
        for business in businesses:
            bus_info = self.parse_business(business)
            info.append(bus_info)
        return info

    def parse_business(self, business):
        bus_info = {
            "name": business["name"]
            , "id": business["id"]
            , "phone": business["display_phone"]
            , "address": business["location"]["address1"]
            , "url": business["url"]
            , "image": business["image_url"]
        }
        return bus_info

    
def main():
    yelp = Yelp()
    req = yelp.business_search()
    # yelp.jprint(req)
    # yelp.jprint(yelp.get_info(req))
    id_req = yelp.id_search("gt1BSfVFvzI-qHdJ3LUZug")
    yelp.jprint(yelp.parse_business(id_req))


if __name__ == "__main__":
    main()