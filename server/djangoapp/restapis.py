import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    if 'apikey' in kwargs:
        try:   #get with authentication
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey',kwargs['apikey']))
        except:
            print("Network exception occurred")
    else:
        try:   #get without authentication
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            print(dealer_doc["short_name"])
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results
def get_dealers_by_state(url, **kwargs):
    results = []
    if "state" not in kwargs: # process as if no params
        return(get_dealers_from_cf(url))
    # Call get_request with a URL and state parameters
    json_result=get_request(url,"state="+kwargs("state"))
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
     #       dealer_doc = dealer["doc"]
            print(dealer_doc["short_name"])
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    if "dealerId" not in kwargs: # cannot process 
        return("")
    # Call get_request with a URL and state parameters
    param=kwargs["dealerId"]
    json_result=get_request(url,dealership=param)
    if json_result:
        reviews = json_result
        # For each review object
        for review_doc in reviews:
    #        print("Here", review_doc)
            # Get its content in `doc` object
     #       dealer_doc = dealer["doc"]
            # Create a review object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                   review=review_doc["review"], purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                   car_model=review_doc["car_model"],
                                   car_year=review_doc["car_year"], _id=review_doc["_id"])
            review_obj.sentiment=analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    print(results)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    params=dict()
    params["text"] = dealerreview
    params["version"] = "20220407"
    params["features"] = "keywords,entities&entities.emotion=true&entities.sentiment=true&keywords.emotion=true&keywords.sentiment=true"
    api_key="pwwxIL6PFiihRJb826t4CoqKwf4Huy_NCIw5sD6RnEiI"
    url="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2fb43dc0-22a9-480e-a641-6bd13ad34b23/v1/analyze"
    #params["return_analyzed_text"] = "kwargs["return_analyzed_text"]"
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
    print("response", response.status_code)
    return(response.sentiment)




