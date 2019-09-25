#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 19:52:43 2019

@author: izzykiver
"""

import requests
import json
 
web_url = "https://www.yelp.com/biz/gobi-mongolian-bbq-sunnyvale"
  
# URL of the web page to be downloaded is defined as web_url
r = requests.get(web_url) # create HTTP response object 
  
# send a HTTP request to the server and save 
# the HTTP response in a response object called r 
#with open("yelp_reviews.html",'wb') as f: 
  
    # Saving received content as a html file in 
    # binary format 
  
    # write the contents of the response (r.content) 
    # to a new file in binary mode. 
   # f.write(r.content) 

URL_list = []

#print(r.text.index("<a href=\"/user_details?userid="))

#The beginning and end value of the substring
review_number = 1
while True: 
    r = requests.get(web_url + "?start=" + str(review_number))
    review_number = review_number + 20
    error_message = r.text.find("Whoops! It doesn’t look like there are any reviews that match" + 
                "the sort or language filters you’ve chosen. Sorry about that.")
    if error_message >=  0:
       break
    k:int = 0
    k1:int = 0
    k2:int = 0
    while True:
        k1 = r.text.find("<a href=\"/user_details?userid=", k)
        if k1 < 0:
            break
        k1 = k1 + 9
        k2 = r.text.index("\"", k1)
        user = r.text[k1 : k2]
        print(user)
        URL_list.append(user)
        k = k2
    break

destination_param = "1135+Tasman+Dr+Sunnyvale+CA"
find_user_location = "<h3 class=\"user-location alternate\">"

travel_n_time = []

class TT:
    def __init__(self, travel, time):
        self.travel = travel
        self.time = time


for value in URL_list:
    user_profile = requests.get("https://www.yelp.com" + value)
    r = user_profile
        # Saving received content as a html file in 
    # binary format 
  
    # write the contents of the response (r.content) 
    # to a new file in binary mode.     
    #with open("yelp_reviews.html",'wb') as f:
    #   f.write(r.content) 
    #break
    find_user_location1:int = r.text.find(find_user_location)
    find_user_location2:int = r.text.find("</h3>", find_user_location1)
    user_location = r.text[find_user_location1 + len(find_user_location) : find_user_location2]
    print(user_location)
    #print(find_user_location1)
    #print(find_user_location2)
    response = requests.get(
        'https://maps.googleapis.com/maps/api/distancematrix/json',
        params={"destinations" : destination_param, "origins" : user_location, "key" : "AIzaSyBLkzq3dSTUnrGXnIUcFEDzXMy0z0Dm00U"},
               )
    #To view the URL output for debugging:
    #print(response.request.url)
    print(response.text)
    
    parsed_json = json.loads(response.text)
    travel = round(parsed_json['rows'][0]['elements'][0]['distance']['value'] * 0.000621371, 2)
    time =   round(parsed_json['rows'][0]['elements'][0]['duration']['value'] / 60, 0)

    travel_n_time.append(TT(travel, time))
    print(str(travel) + "," + str(time) + ",\"" + user_location + "\"")
    
    #export this as csv... then run visualization through python ds tools or on a maps and have it plotted out....

