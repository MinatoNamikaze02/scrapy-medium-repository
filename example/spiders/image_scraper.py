import scrapy
from example.items import ImageScraperItem

class ImageScraperSpider(scrapy.Spider):
    name = 'image_scraper'
    allowed_domains = ['quotefancy.com']
    start_urls = ['https://quotefancy.com/motivational-quotes']
    base_link = 'https://quotefancy.com/motivational-quotes'
    max_pages = 1


    def parse(self, response):
        #images_urls
        obj = ImageScraperItem()
        if response.status == 200:
            #This query only returns the first image
            rel_img_urls = response.css('img').getall()
            #This returns all other images
            rel_secondary_urls = response.css('img').xpath('@data-original').getall()
            rel_img_urls.extend(rel_secondary_urls)
            #Finding number of pages
            number_of_pages = response.xpath('//a[@class="loadmore page-number"]/text()').getall()
            obj['image_urls'] = self.url_join(rel_img_urls, response)
            yield obj
            #If the number_of_pages length is 1, then it means that there is only one page extra
            if len(number_of_pages) == 1:
                self.max_pages = (number_of_pages[0])
            else: 
                #finding the max
                number_of_pages = [int(x) for x in number_of_pages]
                self.max_pages = str(max(number_of_pages))
                # print(self.max_pages)
        # updating link
        next_page = self.base_link + '/page/' + str(self.max_pages)
        # callback for the next page
        yield scrapy.Request(next_page, callback=self.parse)

    # converting relative to absolute URLS
    def url_join(self, rel_img_urls, response):
        urls = [response.urljoin(x) for x in rel_img_urls]
        return urls
