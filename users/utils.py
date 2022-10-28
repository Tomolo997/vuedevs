import random
import string
from .models import Business, Developer ,Verifications,Customer
# get random password pf length 8 with letters, digits, and symbols
def generate_random_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for i in range(8))
    return code

def get_business(user):
    try:
        return Business.objects.get(user=user)
    except Business.DoesNotExist:
        return False

def get_customer(user):
    try:
        return Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return False

def get_developer(user):
    try:
        return Developer.objects.get(user=user)
    except Developer.DoesNotExist:
        return False

def get_developer_or_business_from_id(id):
    business = Business.objects.filter(id=id).values()
    developer = Developer.objects.filter(id=id).values()

    if business:
        return business[0]['name']
    elif developer:
        return developer[0]['name']
    else:
        return False


def changetimezone(timezone):
        timezones = {
            "-12": "-12:00",
            "-11": "-11:00",
            "-10": "-10:00",
            "-09": "-09:00",
            "-08": "-08:00",
            "-07": "-07:00",
            "-06": "-06:00",
            "-05": "-05:00",
            "-04": "-04:00",
            "-03": "-03:00",
            "-02": "-02:00",
            "-01": "-01:00",
              "0": "+00:00",
              "1": "+01:00",
              "2": "+02:00",
              "3": "+03:00",
              "4": "+04:00",
              "5": "+05:00",
              "6": "+06:00",
              "7": "+07:00",
              "8": "+08:00",
              "9": "+09:00",
             "10": "+10:00",
             "11": "+11:00",
             "12": "+12:00",
        }
        return timezones[timezone]