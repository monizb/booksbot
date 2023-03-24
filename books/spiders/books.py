# -*- coding: utf-8 -*-
import scrapy
import json
import re

class GlassdoorReviewSpider(scrapy.Spider):
    name = 'glassdoor_review_spider'
    allowed_domains = ['www.glassdoor.com']
    start_urls = ['https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse, errback=self.handle_error)

    def parse(self, response):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
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
            
    def handle_error(self, response):
        if response.status == 403:
            self.logger.warning('Received 403 Forbidden response')
            # Handle 403 response here
            # ...
        else:
            self.logger.warning('Received response with status code %d', response.status)

