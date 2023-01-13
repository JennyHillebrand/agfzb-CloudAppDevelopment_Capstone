from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name=models.CharField(null=False, max_length=30)
    description=models.CharField(max_length=50)
    def __str__(self):
        return self.name + " - " + \
               self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carmake=models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealership=models.IntegerField()
    name=models.CharField(null=False, max_length=30)
    SUV='suv'
    HATCHBACK='hatchback'
    SEDAN='sedan'
    WAGON='wagon'
    TYPE_CHOICES = [
        (SUV, 'Suv'),
        (HATCHBACK, 'Hatchback'),
        (SEDAN, 'Sedan'),
        (WAGON, 'Wagon')
    ]
    _type=models.CharField(
        null=False, max_length=20, choices=TYPE_CHOICES,
        default=SEDAN
    )
    year=models.IntegerField()
    
    def __str__(self):
        return self.name + " (" + \
               self.carmake.name + ")"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
