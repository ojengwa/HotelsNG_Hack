import json
import ast
import re


out = open('data.out', 'a')

with open('weights.json') as weights_file:
    weights = ast.literal_eval(weights_file.read())


def get_feature_weight(data, value, cancelled):
    if data == 'email_address':
        return getEmailWeight(data, value, cancelled)
    elif data == 'special_request_made':
        return getSpecialRequestWeight(data, value, cancelled)
    elif data == 'cab_service_req':
        return getCabWeight(data, value, cancelled)
    elif data == 'is_phone_booking':
        return getPhoneBookingWeight(data, value, cancelled)
    elif data == 'number_of_rooms':
        return getRoomWeight(data, value, cancelled)
    else:
        return 0


def getCabWeight(key, value, cancelled):
        # cab =  entry["cab_service_req"]
        # cancelled =  entry["cancelled"]
        if (value == '0' and cancelled == '0'):
            return weights["cab_service_req"][(0,0)]
        elif (value == '0' and cancelled == '1'):
            return weights["cab_service_req"][(0,1)]
        elif (value == '1' and cancelled == '0'):
            return weights["cab_service_req"][(1,0)]
        elif (value == '1' and cancelled == '1'):
            return weights["cab_service_req"][(1,1)]


def getPhoneBookingWeight(key, value, cancelled):
    # isPhone =  entry["is_phone_booking"] | 0
    # cancelled =  entry["cancelled"]
    print(type(value))
    if (value == '0' and cancelled == '0'):
        return weights["is_phone_booking"][(0,0)]
    elif (value == '0' and cancelled == '1'):
        return weights["is_phone_booking"][(0,1)]
    elif (value == '1' and cancelled == '0'):
        return weights["is_phone_booking"][(1,0)]
    elif (value == '1' and cancelled == '1'):
        return weights["is_phone_booking"][(1,1)]


def getRoomWeight(key, value, cancelled):
    # noOfRooms =  str(entry["number_of_rooms"])
    # cancelled =  entry["cancelled"]
    if (value < 2 and cancelled == '0'):
        return weights["number_of_rooms"][(1,0)]
    elif (value < 2 and cancelled == '1'):
        return weights["number_of_rooms"][(1,1)]
    elif (value < 6 and cancelled == '0'):
        return weights["number_of_rooms"][(1,0)]
    elif (value < 6 and cancelled == '1'):
        return weights["number_of_rooms"][(1,1)]
    elif (value > 5 and cancelled == '0'):
        return weights["number_of_rooms"][(5,0)]
    elif (value > 5 and cancelled == '1'):
        return weights["number_of_rooms"][(5,1)]


def isPublicEmail(email):
  email = email.lower()
  return re.search('@gmail', email) or re.search('@yahoo', email) or re.search('@live', email) or re.search('@rocketmail', email) or re.search('@hotmail', email) or re.search('@aol', email)


def getEmailWeight(key, data, cancelled):
    value = isPublicEmail(data)
    # cancelled =  entry["cancelled"]
    if (not value and cancelled == '0'):
        print weights["number_of_rooms"][(0,0)]
        return weights["number_of_rooms"][(0,0)]
    elif (not value and cancelled == '1'):
        print weights["number_of_rooms"][(0,1)]
        return weights["number_of_rooms"][(0,1)]
    elif (value and cancelled == '0'):
        print weights["number_of_rooms"][(1,0)]
        return weights["number_of_rooms"][(1,0)]
    elif (value and cancelled == '1'):
        print weights["number_of_rooms"][(1,1)]
        return weights["number_of_rooms"][(1,1)]


def getSpecialRequestWeight(key, value, cancelled):
    # specialRequest =  entry["special_request_made"]
    # cancelled =  entry["cancelled"]
    if (value == 0 and cancelled == '0'):
        return weights["special_request_made"][(0,0)]
    elif (value == 0 and cancelled == '1'):
        return weights["special_request_made"][(0,1)]
    elif (value == 1 and cancelled == '0'):
        return weights["special_request_made"][(1,0)]
    elif (value == 1 and cancelled == '1'):
        return weights["special_request_made"][(1,1)]

with open('dataset.json') as data_file:
    customers = json.load(data_file)
    for customer in customers:
        features = ''
        for feature in customer:
            if weights.has_key(feature):
                # print(feature)
                feature_weight = get_feature_weight(feature, customer[feature],
                                                    str(customer['cancelled']))
                features += str(feature_weight) + ', '
        if features:
            features += str(customer['cancelled'])
            out.write(features + '\n')


