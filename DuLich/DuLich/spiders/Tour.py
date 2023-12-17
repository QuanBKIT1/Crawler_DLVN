import scrapy
from DuLich.items import DulichItem

class TourSpider(scrapy.Spider):
    name = "Tour"
    allowed_domains = ["dulichviet.com.vn"]
    def start_requests(self):
        urls = []
        with open('urls.txt') as file:
            for line in file:
                urls.append(line.rstrip('\n'))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = DulichItem()
        item['title'] = response.xpath('string(//div[@class="tourTitle"])').extract_first()
        item['ticket_ID'] = response.xpath('//div[@class="as"]')[0].xpath('.//text()').extract_first()
        item['trip'] = response.xpath('string(//div[@class="content"]//tr[1]//td[2])').extract_first()
        item['price'] = response.xpath('string(//div[@id="giactt"])').extract_first()
        item['description'] = response.xpath('string(//div[@class="content"]/p)').extract_first()
        item['departure_place'] = response.xpath('//div[@class="as"]')[4].xpath('.//text()').extract_first()
        item['duration'] = response.xpath('//div[@class="as"]')[1].xpath('.//text()').extract_first()
        item['vehicle'] = response.xpath('//div[@class="as"]')[3].xpath('.//text()').extract_first()
        item['time_depart'] = response.xpath('string(//div[@class="content"]//tr[3]//td[2])').extract_first()
        item['highlights'] = response.xpath('string(//div[@class="attr"]/p)').extract_first()
        item['tour_des'] = response.xpath('string(//div[@class="listDay"])').extract_first()
        item['service_des'] = response.xpath('string(//div[@class="content service-more-content"]//p)').extract_first()
        item['view'] = response.xpath('//div[@class="rating-tt"]/i[@class="fa fa-eye"]/following-sibling::text()').extract_first()
        item['url'] = response.url
        item['related_urls'] = response.xpath('//h2[@class="mda-name"]/a/@href').extract()
        item['image_url'] = response.xpath('//div[@class="img"]/img/@src').extract_first()
        
        return item
