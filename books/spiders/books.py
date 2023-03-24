# -*- coding: utf-8 -*-
import scrapy
import json
import re

class GlassdoorReviewSpider(scrapy.Spider):
    name = 'glassdoor_review_spider'
    allowed_domains = ['www.glassdoor.com']
    start_urls = ['https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm']

    def parse(self, response):
        # Extract the JSON data containing the reviews from the page
        json_data = re.search('({"employerId":.*?})', response.text).group(1)
        data = json.loads(json_data)

        # Extract the reviews from the JSON data
        reviews = data['reviews']

        for review in reviews:
            # Extract the review title, rating, and text
            title = review['jobTitle']
            rating = review['ratingNumber']
            text = review['pros'] + ' ' + review['cons']

            # Create a dictionary with the extracted data
            data = {'title': title, 'rating': rating, 'text': text}

            # Yield the dictionary as a Scrapy item
            yield data

        # Follow the "next page" link to scrape additional reviews
        next_page = data['paging']['nextUrl']
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

