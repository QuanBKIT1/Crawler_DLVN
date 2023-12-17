import scrapy
from Vietnambooking.items import TravelItem

class TourSpider(scrapy.Spider):
    name = "Tour"
    allowed_domains = ["www.vietnambooking.com"]
    # start_urls = ["https://travel.com.vn/du-lich-viet-nam/tour-mien-bac.aspx"]
    start_urls = [
                  "https://www.vietnambooking.com/du-lich-trong-nuoc.html",
                # "https://www.vietnambooking.com/du-lich-nuoc-ngoai.html"
                  ]


    def parse(self, response):
        urls = response.xpath('//h3[@class="title-h3"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_page_detail)
        
        # Find next button
        next_page_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page_url is not None:
            print("I am in          " + response.urljoin(next_page_url))
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_page_detail(self, response):
        item = TravelItem()

        item['title'] = response.xpath('string(//h1[@class="title-tour"])').extract_first()
        # 'Tour Du Lịch Bình Hưng 2 Ngày 2 Đêm Trọn Gói'

        item['ticket_ID'] = response.xpath('string(//span[@class="id-tour"])').extract_first()
        # '\r\n                                        VNBHCMBIH2N2D-TTTG-182447                                    '

        item['price_old'] = response.xpath('string(//div[@class="title-price-old"]/del)').extract_first()
        # '4,403,000 VND'
        
        item['price'] = response.xpath('string(//span[@class="price-tour"])').extract_first()
        #  '2,590,000 '
            
        item['description'] = response.xpath('string(//div[@class="single-box-excerpt"]/p)')[0].extract()
        # '\r\n\tĐặt ngay tour\xa0Bình Hưng 2 ngày 2 đêm, xe giường nằm trọn gói giá rẻ\xa0của Vietnam Booking, Quý khách\xa0được khám phá một hòn đảo trong Tứ Bình nổi tiếng, nơi vẹn nguyên nét đẹp\xa0của\xa0thiên nhiên biển đảo\xa0hoang sơ, thơ mộng.\r\n'

        tlb_info_tour = response.xpath('//table[@class="tlb-info-tour"]//tr')
        item['departure_place'] = tlb_info_tour[0].xpath('.//td')[0].xpath('string(.)').extract_first()
        # ' \r\n                                Hồ Chí Minh'

        item['duration'] = tlb_info_tour[0].xpath('.//td')[1].xpath('string(.)').extract_first()
        # ' 2 ngày 2 đêm '

        item['vehicle'] = tlb_info_tour[0].xpath('.//td')[2].xpath('./img/@title').extract()
        #  ['Xe', 'Tàu thủy']

        item['time_depart'] = tlb_info_tour[2].xpath('.//span/text()').extract_first()

        item['services'] = response.xpath('.//ul[@class="list-extra-services"]/li/text()').extract()
        # ['\xa0\xa0Bảo hiểm', '\xa0\xa0Bữa ăn', '\xa0\xa0Hướng dẫn viên', '\xa0\xa0Vé tham quan', '\xa0\xa0Xe đưa đón']

        item['highlights'] = response.xpath('string(//div[@class="single-box-excerpt"]/ul)').extract_first()
        # ['Tour có hướng dẫn viên chụp hình rất có tâm và có tầm.', 'Setup free các vật dụng để cho du khách chụp hình: Trái cây bãi biển,\xa0phao vịt hồng và vàng, sao biển và\xa0ván Sup cực chill trên biển.', 'Trải nghiệm chèo thuyền KAYAK free.', 'Nhiều view chụp hình trên Nhà Hàng Bè Nổi: Trái Tim Chung Đôi, Vòng Hoa, Võng Bánh Bèo View Biển, View Biển Lưới sang chảnh, Xích Đu,...', 'Đồi Cừu Suối Tiên với những chú cừu trắng trên cánh đồng, điểm tô thêm là Vòng Hoa - Xe Màu Vàng và cây cầu giữa đồng ruộng hoặc ghé thăm Hang Rái.', 'Tham quan Vườn Nho Thái An - Ninh Thuận - khách được thử nho chín tại vườn và thử Rượu Nho - Mật Nho và Mứt Nho (Free), được tự tay hái nho mang về làm quà.', 'Chinh phục cung đường ven biển đẹp nhất Nam Trung Bộ - Vĩnh Hy.', 'Tham quan Bãi Đá Trứng buổi chiều trên đảo.', 'Trải nghiệm lướt trên mặt sóng với CANO: Mới, sang - xịn - mịn.', 'Ưu tiên sử dụng xe giường nằm Cabin riêng biệt (VIP cabin) của PHƯƠNG TRANG BUS khi đặt tour sớm.']

        item['tour_des'] = response.xpath('string(//div[@class="panel-body content-tour-item content-tour-tab-program-tour-0"])').extract_first()
        # ...

        item['adult_price'] = response.xpath('string(//*[@id="table-price-1"]/div[1]/table/tbody/tr[2]/td[2])').extract_first()
        # ['\r\n\t\t\t\t', '\r\n\t\t\t\t\t', '2.590.000', '\r\n\t\t\t\t', '\r\n\t\t\t'] 

        item['chidren_price'] = response.xpath('string(//*[@id="table-price-1"]/div[1]/table/tbody/tr[2]/td[3])').extract_first()
        
         
        item['baby_price'] = response.xpath('string(//*[@id="table-price-1"]/div[1]/table/tbody/tr[2]/td[4])').extract_first()
        # ['\r\n\t\t\t\t', 'Liên hệ', '\r\n\t\t\t']
        item['service_des'] = response.xpath('//*[@id="table-price-1"]/div[1]/*')[1:].xpath("string(.)").extract()
        

        yield item  