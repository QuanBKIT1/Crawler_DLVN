import scrapy
from Vietnambooking.items import BlogItem

class BlogSpider(scrapy.Spider):
    name = "Blog"
    allowed_domains = ["www.vietnambooking.com"]
    start_urls = ["https://www.vietnambooking.com/du-lich/blog-du-lich"]

    def parse(self, response):
        urls = response.xpath('//div[@class="category-box-list-default-inner"]//li/h3/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_page_detail)
        
        # Find next button
        next_page_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page_url is not None:
            print("I am in          " + response.urljoin(next_page_url))
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
    
    def parse_page_detail(self, response):
        item = BlogItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['url'] = response.url
        item['content'] = '\n'.join(response.xpath('//div[@class="single-box-content-inner"]')[0].xpath('.//text()').extract())
        return item