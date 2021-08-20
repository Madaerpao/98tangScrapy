# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossproItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    href = scrapy.Field()
    type = scrapy.Field()
    ny_name = scrapy.Field()
    img_link = scrapy.Field()
    magenet = scrapy.Field()
    hot = scrapy.Field()
    fm_img_link = scrapy.Field()
    pass
