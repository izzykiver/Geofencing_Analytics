#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 19:52:43 2019

@author: izzykiver
"""
#bs4 / beautiful soup
import requests
import json
import csv

# ##################################
# ARGUMENTS
# ##################################

urlStartPage = "https://www.yelp.com/biz/gobi-mongolian-bbq-sunnyvale"
locReferenceLocation = "1135+Tasman+Dr+Sunnyvale+CA"
minTravelMiles = 0
maxTravelMiles = 200
nChartBars = 10
sSaveUserUris = "save_user_uris.csv"
sSaveUserLocs = "save_user_locs.csv"
sSaveTravels  = "save_travels.csv"
sSaveRanges   = "save_ranges.csv"

# ##################################
# UTILITIES
# ##################################

def dbgSavePage(resPageToSave, sFileName):
  with open(sFileName,'wb') as f:
    f.write(resPageToSave.content)
# end of def dbgSavePage()

class SubstringLocation:
  def __init__(self):
    self.k1: int = 0
    self.k2: int = 0

  def reset(self):
    self.k1 = 0
    self.k2 = 0
# end of class SubstringLocation

class SubstringFinder:
  def __init__(self, source: str, before: str, beforeSkip: int, beforeSkipFromHead: bool, after: str):
    self.source            : str  = source
    self.before            : str  = before
    self.beforeSkip        : int  = beforeSkip
    self.beforeSkipFromHead: bool = beforeSkipFromHead
    self.after             : str  = after
    # just an optimization to avoid getting the lengths
    # every time getNextSubstring() is called
    self.beforeLen: int = len(self.before)
    self. afterLen: int = len(self.after )
    self.location: SubstringLocation = SubstringLocation()
  # end of def __init__()

  def reset(self, source: str):
    self.source = source
    self.location.reset()

  def getNextSubstring(self) -> str:
    # nothing to find if the last search did not find a substring
    if self.location.k1 < 0: return None
    # search for the beginning of the substring after the end of the last
    self.location.k1 = self.source.find(self.before, self.location.k2)
    if self.location.k1 < 0: return None # nothing found
    # search for the end of the substring after the beginning
    # differently from find(), index() throws an error if nothing is found
    k: int = self.location.k1 + self.beforeLen
    self.location.k2 = self.source.index(self.after, k)
    found: str = self.source[
      (self.location.k1 + self.beforeSkip
        if self.beforeSkipFromHead
        else k - self.beforeSkipFromHead)
    : self.location.k2]
    # prepare for the next search
    self.location.k2 = self.location.k2 + self.afterLen
    return found
  # end of def getNextSubstring()
# end of class SubstringFinder

# ##################################
# FETCH START PAGE
# ##################################

#pulls the start page and downloads to file
resStartPage = requests.get(urlStartPage)
dbgSavePage(resStartPage, "resStartPage.html")

# ##################################
# EXTRACT THE USER URIs FROM THE REVIEW PAGES
# ##################################

# store the user URIs in a set to remove duplicates
uriUserPages = set()

# extract and save user URIs to file
with open(sSaveUserUris,'wt') as fSaveUserUris:
  fSaveUserUris.write("user_uri\n")
  iFirstReviewInPage = 1
  while True:
    # fetch the review page
    urlReviewsPage = urlStartPage + "?start=" + str(iFirstReviewInPage)
    print(urlReviewsPage)
    resReviewsPage = requests.get(urlReviewsPage)
    iFirstReviewInPage = iFirstReviewInPage + 20
    # check whether this was the last review page (k return the index if the message was found)
    kEndOfReviews = resReviewsPage.text.find("Whoops! It doesn’t look like" +
      "there are any reviews that match the sort" +
      "or language filters you’ve chosen. Sorry about that.")
    if kEndOfReviews >= 0: break
    # extract the user URIs from the review page
    finderUserPages = SubstringFinder(resReviewsPage.text, "\"/user_details?userid=", 1, True, "\"")
    while True:
      uriUserPage = finderUserPages.getNextSubstring()
      if uriUserPage == None: break
      print("  ", uriUserPage)
      # save the user URI
      fSaveUserUris.write("\"" + uriUserPage + "\"\n")
      # add the user URI to the set
      uriUserPages.add(uriUserPage)
    if len(uriUserPages) > 120: break # TO DELETE
    break # TO DELETE
  # end of while: fetch review page
# end of with open(strSaveUserUris)

# ##################################
# FIND THE USER LOCATIONS FROM THE USER PAGES
# ##################################

class LocationInfo:
  def __init__(self, locUserLocation):
    self.locUserLocation = locUserLocation
    self.nUserCount = 1
    self.miles   = -1
    self.minutes = -1
# end of class LocationInfo

# map of unique location -> number of users from that location
locations = dict()

with open(sSaveUserLocs,'wt') as fSaveUserLocs:
  fSaveUserLocs.write("user_uri,location\n")
  finderUserLocation = SubstringFinder("", "<h3 class=\"user-location alternate\">", 0, False, "</h3>")
  for uriUserPage in uriUserPages:
    # fetch the user page
    resUserPage = requests.get("https://www.yelp.com" + uriUserPage)
    # find the user location in the user page
    finderUserLocation.reset(resUserPage.text)
    locUserLocation = finderUserLocation.getNextSubstring()
    print(locUserLocation)
    # save the user location
    fSaveUserLocs.write("\"" + uriUserPage + "\",\"" + locUserLocation + "\"\n");
    # increment the user count for the location
    if locUserLocation in locations:
      locations[locUserLocation].nUserCount += 1
    else:
      locations[locUserLocation] = LocationInfo(locUserLocation)
  # end of for uriUserPage
# end of with open(sSaveUserLocs)

# ##################################
# FIND THE TRAVEL TIMES AND DISTANCES
# ##################################

with open(sSaveTravels,'wt') as fSaveTravels:
  fSaveTravels.write("miles,minutes,count,location\n")
  finderUserLocation = SubstringFinder("", "<h3 class=\"user-location alternate\">", 0, False, "</h3>")
  for location in locations.values():
    # use Google's API to find the travel distance and time from the user location to the reference location
    resTravel = requests.get(
      'https://maps.googleapis.com/maps/api/distancematrix/json',
      params = {
        "origins"     : location.locUserLocation,
        "destinations": locReferenceLocation,
        "key": "AIzaSyBLkzq3dSTUnrGXnIUcFEDzXMy0z0Dm00U"
      }
    )
    jsonTravel = json.loads(resTravel.text)
    location.miles   = round(jsonTravel['rows'][0]['elements'][0]['distance']['value'] * 0.000621371, 2)
    location.minutes = round(jsonTravel['rows'][0]['elements'][0]['duration']['value'] / 60, 0)
    print(location.miles, ", ", location.minutes,
      ", ", location.nUserCount, ", [" + location.locUserLocation + "]")
    # save the travel distance and time for the user location
    fSaveTravels.write(str(location.miles) + "," + str(location.minutes) +
      "," + str(location.nUserCount) + ",\"" + location.locUserLocation + "\"\n")
  # end of for uriUserPage
# end of with open(sSaveTravels)

# ##################################
# COUNT THE TRAVEL DISTANCES IN EACH RANGE
# ##################################

class ChartRange:
    def __init__(self, rangeStart, rangeEnd):
        self.start = rangeStart
        self.end   = rangeEnd
        self.nDataPointsInRange: int = 0

chartRanges = []

# initialize chartRanges
rangeInterval = (maxTravelMiles - minTravelMiles) / nChartBars
rangeStart = minTravelMiles
for iChartBar in range(0, nChartBars):
  start = rangeStart
  rangeStart += rangeInterval
  end   = rangeStart
  chartRanges.append(ChartRange(start, end))
# end of for iChartBar

# sort and count the data points into the ranges
for location in locations.values():
  for range in chartRanges:
    if location.miles >= range.start and location.miles < range.end:
      range.nDataPointsInRange += location.nUserCount

# save the ranges
with open(sSaveRanges,'wt') as fSaveRanges:
  fSaveRanges.write("count,start,end\n")
  for range in chartRanges:
    print(range.nDataPointsInRange, " [", range.start, ", ", range.end, ")")
    fSaveRanges.write(str(range.nDataPointsInRange) + "," + str(range.start) + "," + str(range.end) + "\n")
# end of with open(sSaveRanges)
