import json
from re import L
from turtle import color
from unicodedata import name
import scrapy


class MangoSpider(scrapy.Spider):
    name = "mango"
    start_urls = [
        'https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99'
    ]
    headers={
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "stock-id": "068.IN.0.true.false.v0"
        }
    
    def parse(self, response):
        url = 'https://shop.mango.com/services/garments/1704202099'

        yield scrapy.Request(url, callback=self.parse_api, headers=self.headers)

    def parse_api(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        
        id_item = self.start_urls[0][-2:]
        color_id = id_item

        #finding selected color
        # for i  in range(len(data['colors']['colors'])):
        #     if data['colors']['colors'][i]['id']==id_item:
        #         color_id = i

        #finding default
        for i  in range(len(data['colors']['colors'])):
            if 'default' in data['colors']['colors'][i]:
                color_id = i

        sizes = list()
        for size in data['colors']['colors'][color_id]['sizes']:
            if size['value']!='0':
                sizes.append(size['label'])
        
        info =  {
            "name" : data['name'],
            "price" : data['price']['price'],
            "color" : data['colors']['colors'][color_id]['label'],
            "size" : sizes
        }

        filename = f"mango-{data['name']}.json"
        with open(filename, 'w') as f:
            json.dump(info,f)
        self.log(f'Saved file {filename}')
         