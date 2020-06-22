# ScrapingDynamicArticles


### Description
This is a scraper page of the site https://hbr.org/insight-center/coronavirus by Scrapy framework.
The file with a spider scrapes data on such fields as:
- article title
- category
- date of publication
- also the spider enters each article and extracts all authors

The page has dynamic content in the form of infinite scrolling, therefore the data is parsed on the basis of the hidden api.  
Spider parses the extracted data into Items where was added pre/post processing to each Item field (via ItemLoader).   
Then the Items go through Item Pipelines for further processing.  
Pipelines were added to work with the database and to exclude duplicates when re-scraping data.  
The database schema has three tables to store these data, i.e., article, category, author.  
There is a many-to-many relationship between article and author and a one-to-many relationship between category and article.

### HOW TO
Use python version 3.8.0 or later.
1. clone this project
2. activate your virtual environment
3. pip install -r requirements.txt
4. run spider by 'scrapy crawl article' command