# Geofencing_Analytics
Scrape YELP page data to find the user profile URL (hint... start 9 characters into the line)
To flip through each Yelp page, modify the URL query to include review offset/start index (Yelp displays 20 at a time so url param would include, 20, 40, etc). 
Scrape user location (similar to step 1)
Insert Google Map Platform API Key for Distance Matrix API 
Parse the JSON of each call result to upload user distance into a CSV
Run analysis to calculate AVG, MIN, MAX, and STD Dev distance of user to restaurant location
Run visualization using python library to display distance traveled by plotting points on Google Map and Bar Graph (Distance Traveled X, User count Y)...
