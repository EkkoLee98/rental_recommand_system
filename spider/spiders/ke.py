from subprocess import call
import scrapy
import re


class KeSpider(scrapy.Spider):
    name = "ke"
    allowed_domains = []
    start_urls = []
    city_url = "https://www.ke.com/city/"

    def start_requests(self):
        yield scrapy.Request(self.city_url)

    def parse(self, response):
        provinces = response.css(".city_province")
        for p in provinces:
            province = p.css("div.c_b::text").extract_first().strip()
            for a in p.css("ul a"):
                city = a.xpath("./text()").extract_first().strip()
                city_url = response.urljoin(a.xpath("./@href").extract_first().strip())
                if "fang" in city_url:
                    continue
                zufang_url = city_url.replace("ke.com", "zu.ke.com/zufang/pg{}/")
                meta = dict(province=province, city=city, url=zufang_url, page=1)
                yield scrapy.Request(
                    meta["url"].format(meta["page"]),
                    meta=meta,
                    callback=self.parse_list,
                )

    def parse_list(self, response):
        meta = response.meta

        for i in response.css(".content__list--item"):
            item = dict()
            item["cover"] = response.urljoin(
                i.css(".content__list--item--aside img::attr(data-src)").extract_first()
            )
            item["title"] = i.css(".twoline::text").extract_first().strip()
            if not item["title"]:
                continue
            item["type"] = item["title"].split("·")[0].strip()
            item["url"] = response.urljoin(
                i.css(".twoline::attr(href)").extract_first()
            )
            item["oid"] = item["url"].split(".html")[0].split("/")[-1]
            des = (
                i.xpath("string(.//p[@class='content__list--item--des'])")
                .extract_first()
                .strip()
            )
            des = [d.strip() for d in des.split("/") if d.strip() != "精选"]
            item["location"] = des[0]
            item["area_text"] = des[1]
            item["area"] = float(re.search(r"(\d+\.\d+)", des[1]).group(1))
            item["orientation"] = des[2]
            item["structure"] = des[3]
            item["price_text"] = (
                i.xpath("string(.//*[@class='content__list--item-price'])")
                .extract_first()
                .strip()
            )
            item["tags"] = ",".join(
                i.css(".content__list--item--bottom i::text").extract()
            )
            item["price"] = int(item["price_text"].split(" ")[0])
            try:
                item["level"], item["floor"] = re.split(
                    "\s+", des[4].replace("（", "").replace("）", "")[:-1]
                )
                item["floor"] = int(item["floor"])
            except:
                pass
            meta["item"] = item
            yield scrapy.Request(item["url"], meta=meta, callback=self.parse_detail)
        if meta["page"] < 10:
            meta["page"] += 1
            yield scrapy.Request(
                meta["url"].format(meta["page"]),
                meta=meta,
                callback=self.parse_list,
            )

    def parse_detail(self, response):
        meta = response.meta
        item = meta["item"]
        item["province"] = meta["province"]
        item["city"] = meta["city"]
        item["imgs"] = "\n".join(
            response.css(".content__article__slide__item img::attr(data-src)").extract()
        )
        detail = response.css(".content__article__info").extract_first()
        detail += response.css(".content__article__info2").extract_first()
        detail += response.css(".cost_content").extract_first()
        item["detail"] = detail
        yield item
