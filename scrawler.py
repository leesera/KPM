import scrapy
from scrapy.http.request import Request

class PackSpider(scrapy.Spider):
  name = 'packspider'
  program = "bash"
  start_urls = ["https://launchpad.net/ubuntu/+source/%s/+publishinghistory" % (program)]
  main_url = "https://launchpad.net/"
  allowed_domains = ["launchpad.net"]

  def parse_link(self,response):
    try:
      print("parse_link",response)
      print("in")
      print("response")
      ret = response.meta['item']
      print(ret)
      text = response.css("a.download::text").extract()
      href = response.css("a.download::attr(href)").extract()
      links ={}
      for idx, val in enumerate(text):
        links[val] = href[idx]
      ret['links'] =links 
      yield ret
    except Exception as e:
      print e
      pass



  def parse(self, response):
    print("parse",response)
    for title in response.xpath("//table[@id='publishing-summary']/tbody/tr"):
      idx_status = 1
      try:
        tr = title
        target, version = tr.css("td a::text").extract()
        ret = {}
        ret['target'] = target
        ret['version'] = version
        link = self.main_url + tr.css("td a[href*=source]::attr(href)").extract()[1]
        request = Request(link,self.parse_link)
        request.meta['item'] = ret
        yield request
      except  Exception as e:
        #print e
        pass
      #self.parse_tr(title)

    for next_page in response.css('a.next'):
      yield response.follow(next_page, self.parse)
