# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import xlwt
import re
# import pymysql
ex = re.compile('【出演女优】：(.+)')
class BossproPipeline:
    workbook = None
    wuma_times = 1
    youma_times = 1
    def open_spider(self,spider):
        print("开始…………")
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet1 = self.workbook.add_sheet('sheet1')
        self.sheet2 = self.workbook.add_sheet('sheet2')
        col = ['编号','类型','女优','片名','热度','种子链接','封面链接','预览链接','原帖链接']
        for i in range(0,9):
            self.sheet1.write(0,i,col[i])
            self.sheet2.write(0,i,col[i])
        # self.conn = pymysql.connect(user='root',password='me1a1qin9.',host='159.75.49.102',database='spider',port=3306)
        # self.curser = self.conn.cursor()
        # print("数据库链接成功，开始写入信息！！！！")
    def process_item(self, item, spider):
        if item['type'] == '无码高清':
            content = []
            count = self.wuma_times
            content.append(count)
            type = item['type']
            content.append(type)
            if len(re.findall(ex,item['ny_name'])) != 0:
                ny_name = re.findall(ex,item['ny_name'])[0]
            content.append(ny_name)
            title = item['title']
            content.append(title)
            hot = int(item['hot'])
            content.append(hot)
            magenet = item['magenet']
            content.append(magenet)
            fm_img_link = item['fm_img_link']
            content.append(fm_img_link)
            img_link = item['img_link']
            content.append(img_link)
            href = item['href']
            content.append(href)
            for i in range(0,9):
                self.sheet2.write(count,i,content[i])
            self.wuma_times += 1
            return item
            # content = []
            # # count = self.wuma_times
            # # content.append(count)
            # # type = item['type']
            # # content.append(type)
            # if len(re.findall(ex, item['ny_name'])) != 0:
            #     ny_name = "'" + re.findall(ex, item['ny_name'])[0] + "'"
            # else:
            #     ny_name = "' '"
            # content.append(ny_name)
            # title = "'"+ item['title'] +"'"
            # content.append(title)
            # hot = "'"+ str(item['hot'])+ "'"
            # content.append(hot)
            # magenet = "'"+str(item['magenet'])+"'"
            # content.append(magenet)
            # if type(item['fm_img_link']) != 'NoneType':
            #     fm_img_link = "'"+str(item['fm_img_link'])+"'"
            # else:
            #     fm_img_link = "' '"
            # content.append(fm_img_link)
            # if type (item['img_link']) != 'NoneType':
            #     img_link = "'"+str(item['img_link'])+"'"
            # else:
            #     img_link = "' '"
            # content.append(img_link)
            # href = "'"+str(item['href'])+"'"
            # content.append(href)
            # sql = '''
            #     INSERT INTO wuma (actress,title,hot,magnet,fmlink,link,href)
            #     VALUE (%s)
            #     '''%",".join(content)
            # self.curser.execute(sql)
            # # self.wuma_times += 1
            # self.conn.commit()
            # return item
        else:
            content = []
            count = self.youma_times
            content.append(count)
            type = item['type']
            content.append(type)
            if len(re.findall(ex,item['ny_name'])) != 0:
                ny_name = re.findall(ex,item['ny_name'])[0]
            content.append(ny_name)
            title = item['title']
            content.append(title)
            hot = int(item['hot'])
            content.append(hot)
            magenet = item['magenet']
            content.append(magenet)
            fm_img_link = item['fm_img_link']
            content.append(fm_img_link)
            img_link = item['img_link']
            content.append(img_link)
            href = item['href']
            content.append(href)
            for i in range(0, 9):
                self.sheet1.write(count, i, content[i])
            self.youma_times += 1
            return item
            # content = []
            # count = self.youma_times
            # content.append(count)
            # type = item['type']
            # content.append(type)
            # if len(re.findall(ex, item['ny_name'])) != 0:
            #     ny_name = "'" + re.findall(ex, item['ny_name'])[0] + "'"
            # else:
            #     ny_name = "' '"
            # content.append(ny_name)
            # title = "'" + item['title'] + "'"
            # content.append(title)
            # hot = "'" + str(item['hot']) + "'"
            # content.append(hot)
            # magenet = "'" + str(item['magenet']) + "'"
            # content.append(magenet)
            # if type(item['fm_img_link']) != 'NoneType':
            #     fm_img_link = "'" + str(item['fm_img_link']) + "'"
            # else:
            #     fm_img_link = "' '"
            # content.append(fm_img_link)
            # if type(item['img_link']) != 'NoneType':
            #     img_link = "'" + str(item['img_link']) + "'"
            # else:
            #     img_link = "' '"
            # content.append(img_link)
            # href = "'" + str(item['href']) + "'"
            # content.append(href)
            # sql = '''
            #     INSERT INTO youma (actress,title,hot,magnet,fmlink,link,href)
            #     VALUE (%s)
            #     '''%",".join(content)
            # self.curser.execute(sql)
            # # self.youma_times += 1
            # self.conn.commit()
            # return item
    def close_spider(self,spider):
        # self.curser.close()
        # self.conn.close()
        self.workbook.save('./高清中文字幕.xls')
        print("结束…………")