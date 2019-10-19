# Geofencing_Analytics

The purpose of this project is to help local business owners spend their marketing dollars more intelligently, by sending their marketing message in the form of location based advertising through mailers, billboards and PPC ads on Facebook/Google to the areas that their customers are currently coming from. This is especially useful for retargeting campaigns and extending the LTV (life-time value) of a customer. 

The project is broken down into two files. A scrapy.py file which downloads the user profiles, locations and compares them against the businesses location using Google Distance Matrix API and a Jupyter Notebook which visualizes how far customers travel, broken down into ranges by miles on a bar graph. 

Summary of operations for Scraping File:

1. Import necessary tools (Json, Requests, & CSV)

2. Define variables for ranges and values. We build clusters and a threshold of how far our out our data is relevant and exclude outliers if needed. Define variables to save results into CSV files.

3. Scrape YELP page data to find the user profile URL 

4. Flip through each Yelp page, modify the URL query to include review offset/start index (Yelp displays 20 at a time so url param would include, 20, 40, etc). 

5. Scrape user location (similar to step 1)

6. Insert Google Map Platform API Key to calculate Distance Matrix API 

7. Parse the JSON of each call result to upload user distance into a CSV

JUPYTER NOTEBOOK

8. Run analysis to calculate AVG, MIN, MAX, and STD Dev distance of user to restaurant location

9. Run visualization using python library to display distance traveled by customer via Bar Graph (Distance Traveled: X, User count: Y)
