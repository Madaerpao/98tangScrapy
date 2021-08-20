import scrapy
from bossPro.items import BossproItem

class BossSpider(scrapy.Spider):
    name = 'boss'
    # allowed_domains = ['www.boss.com']
    start_urls = ['https://www.sdfdsfdsasd.xyz/forum-103-1.html']
    url = 'https://www.sdfdsfdsasd.xyz/forum-103-%d.html'
    num = 2
    def parse_detail(self,response):
        item = response.meta['item']
        td = response.xpath('//body/div[6]/div[6]/div[2]/div[1]//table[1]//div[@class="t_fsz"]//table/tr/td')
        # print(td)
        fm_img_link = td.xpath('./img/@file').extract_first()
        ny_name = td.xpath('.//text()[2]').extract_first().replace("\n", "").replace("\r", "").replace(' ', '')
        img_link = td.xpath('.//ignore_js_op/img/@file').extract_first()
        magenet = td.xpath('./div/div/ol/li/text()').extract_first()
        # print(ny_name,img_link,magenet)
        item['fm_img_link'] = fm_img_link
        item['ny_name'] = ny_name
        item['img_link'] = img_link
        item['magenet'] = magenet
        yield item
        pass
    def parse(self, response):
        tbs = response.xpath('//*[@id="threadlisttableid"]/tbody')
        for tb in tbs:
            item = BossproItem()
            title = tb.xpath('.//tr/th/a[2]/text()').extract()
            if len(title) == 0 or title[0] == '隐藏置顶帖':
                continue
            href = 'https://www.sdfdsfdsasd.xyz/' + tb.xpath('.//tr/th/a[2]/@href').extract()[0]
            type = tb.xpath('.//tr/th/em/a/text()').extract()
            hot = tb.xpath('.//tr/td[@class="num"]/em/text()').extract()
            item['title'] = title[0]
            if len(type) == 0 :
                type = ['有码高清']
                item['type'] = type[0]
            else:
                item['type'] = type[0]
            item['href'] = href
            item['hot'] = hot[0]
            yield scrapy.Request(url=href,callback=self.parse_detail,meta={'item':item})
        if self.num <= 452:
            n_url = format(self.url%self.num)
            self.num += 1
            yield scrapy.Request(url=n_url,callback=self.parse)
