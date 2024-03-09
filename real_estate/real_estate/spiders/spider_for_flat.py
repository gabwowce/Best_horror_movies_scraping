import scrapy
import re

class ButuSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["domoplius.lt"]
    start_urls = ["https://domoplius.lt/skelbimai/butai?page_nr=50"]

    def parse(self, response):
        items = response.css('.item.lt')
        for item in items:
            link = item.css('.thumb.fl a::attr(href)').get()
            price = item.css('.price strong::text').get()
            params = item.css('.param-list div span::text').getall()

            # Follow the link to the detail page, passing item data in the meta
            yield response.follow(link, self.parse_details, meta={'link': link, 'price': price, 'parameters': params})

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_details(self, response):
        # Retrieve the item data passed via 'meta'
        item = response.meta

        # Extract details like condition and heating from the detail page
        condition = response.xpath('//th[contains(text(), "Būklė")]/following-sibling::td/strong/text()').get()
        heating = response.xpath('//th[contains(text(), "Šildymas")]/following-sibling::td/strong/text()').get()
        city = response.xpath('//*[@id="container"]/section/div[1]/div[1]/main/div[3]/div[1]/a/span').xpath('string(.)').get()
        district = response.xpath('//*[@id="container"]/section/div[1]/div[1]/main/div[3]/div[2]/a/span').xpath('string(.)').get()
        street = response.xpath('//*[@id="container"]/section/div[1]/div[1]/main/div[3]/div[3]/a/span').xpath('string(.)').get()

        price = item.get('price', '').replace('€', '').replace(' ', '')
        area = item.get('parameters')[0].replace(' m²', '')
        rooms = item.get('parameters')[1].replace(' kamb.', '')
        year = int(item.get('parameters')[2].replace(' m.', ''))
        floor_info = item.get('parameters')[3].replace(' a.', '')
        floors = re.findall(r'\d+', floor_info)
        floor = floors[0] if floors else ''
        total_floor = floors[1] if len(floors) > 1 else ''
        status = 'Rent' if 'nuoma' in item.get('link') else 'For Sale'


        final_item = {
            'link': item.get('link'),
            'city': city,
            'district': district,
            'street': street,
            'price': price,
            'area': area,
            'rooms': rooms,
            'year': year,
            'floor': floor,
            'total floor': total_floor,
            'condition': condition,
            'heating': heating,
            'status': status
        }

        yield final_item
