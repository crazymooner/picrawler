import scrapy
from datetime import date, datetime
from scrapy.http import Request
from picrawler.items import PicrawlerItem
from scrapy import log
import codecs


class PiSpider(scrapy.Spider):
    name = "pimain"
    allowed_domains = ["zdcj.net"]
    start_urls = [
        "http://www.zdcj.net/reportlist/newreport_1.html",
        "http://www.zdcj.net/reportlist/newreport_2.html",
        "http://www.zdcj.net/reportlist/newreport_3.html",
        "http://www.zdcj.net/reportlist/newreport_4.html",
        "http://www.zdcj.net/reportlist/newreport_5.html",
        "http://www.zdcj.net/reportlist/newreport_6.html",
        "http://www.zdcj.net/reportlist/newreport_7.html",
        "http://www.zdcj.net/reportlist/newreport_8.html",
        "http://www.zdcj.net/reportlist/newreport_9.html",
        "http://www.zdcj.net/reportlist/newreport_10.html",
    ]

    def __init__(self, path, crawlDate=date.today().strftime("%Y-%m-%d")):
        self.crawlDate = datetime.strptime(crawlDate, "%Y-%m-%d").date()
        self.path = path

    def parse(self, response):
        for item in response.xpath('//tbody/tr/td[2]/a[contains(@href, "www.zdcj.net")]'):
            dateStr = item.xpath('../../td[6]/text()').extract()[0]
            currentDate = datetime.strptime(dateStr, "%Y-%m-%d").date()
            log.msg("Crawl Date is {0:%Y-%m-%d}".format(self.crawlDate),
                    level=log.DEBUG)
            log.msg("Record Date is {0:%Y-%m-%d}".format(currentDate),
                    level=log.DEBUG)
            #if artical date is newer then the given date then skip
            if currentDate > self.crawlDate:
                continue
            #if artical date is older then the given date then stop
            if currentDate < self.crawlDate:
                break
            url = item.xpath('@href').extract()[0].encode("utf-8")
            log.msg(url, log.DEBUG)
            yield Request(url, callback=self.parseReport)

    def parseReport(self, response):
        item = PicrawlerItem()
        item['category'] = response.xpath('//div/span[1]/text()').extract()[0]
        item['title'] = response.xpath('//h1/text()').extract()[0]
        item['date'] = response.xpath('//div/span[4]/text()').extract()[0]
        contentArr = response.xpath('//div/p/text()').extract()
        contentStr = ""
        for block in contentArr:
            contentStr = contentStr + block
        item['content'] = contentStr
        log.msg("title: " + item['title'], log.DEBUG)
        log.msg("content: " + item['content'], log.DEBUG)
        outfile = codecs.open(self.path + item['title'], 'w', 'utf-8')
        outfile.write("START\n")
        outfile.write("category: " + item['category'] + "\n")
        outfile.write("title: " + item['title'] + "\n")
        outfile.write("date: " + item['date'] + "\n")
        outfile.write("content: " + item['content'] + "\n")
        outfile.write("END\n")
        outfile.close()
