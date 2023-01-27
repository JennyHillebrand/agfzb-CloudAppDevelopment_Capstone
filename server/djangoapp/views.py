from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)



# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context={}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/fd85c27a-b1ca-4a38-aade-428b130788db/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"]=dealerships
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html',context)
 #   context = {}
 #   if request.method == "GET":
 #       return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    print("yes indeed")
    context={}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/fd85c27a-b1ca-4a38-aade-428b130788db/dealership-package/get-review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        # Concat all dealer's short name
        dealer_reviews=[]
        for review in reviews:
        
            with_sentiment=str(review.review)+" "+str(review.sentiment)
            dealer_reviews.append(with_sentiment)
     #   dealer_reviews = ' '.join([review.review for review in reviews])
        # Return a list of dealer short name
      #  print("dealer reviews",reviews[0])
        context["dealer_reviews"]=reviews
        context["dealer_name"]=review.name 
        context["dealer_id"]=dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context={}
    if request.user.is_authenticated:
        if request.method == "GET":
            car_list=CarModel.objects.filter(dealership=dealer_id)
            cars=[]
            for car in car_list:
                print(car.name, car.carmake, car.year)
                cars.append(car)
            context["cars"]=cars
            context["dealer_id"]=dealer_id
            return render(request, 'djangoapp/add_review.html',context)
        else:
            review={}
            review["review_time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
          #  cardealer=get_object_or_404(CarDealer, pk=dealer_id)
            review["name"]="Nice Name" #cardealer.full_name
            review["review"] = request.POST["content"]
            review["purchase"]=request.POST["purchasecheck"]
            review["purchase_date"]=request.POST["purchasedate"].strftime("%Y")
            car_id=request.POST["car_id"]
            carmodel = get_object_or_404(CarModel, pk=car_id)
            review["car_make"] = carmodel.carmake
            review["car_model"]=carmodel.name
            review["car_year"]=carmodel.year

    # can add extra fields as required
            json_payload={}
            json_payload["review"]=review
            #print("before post review", json_payload)
            response=post_request("https://us-east.functions.appdomain.cloud/api/v1/web/fd85c27a-b1ca-4a38-aade-428b130788db/dealership-package/post-review",\
             review)
            #print("post review status", response.status_code)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)     
    else:
        context['message'] = "Please log in to continue"
        return render(request, 'djangoapp/user_login_bootstrap.html', context)     
# ...

