import scrapy


# Usage: scrapy runspider scraper.py -a scope=all|one
class AyumiloveSpider(scrapy.Spider):
    name = "ayumilove_spider"
    start_urls = ['https://ayumilove.net/raid-shadow-legends-list-of-champions-by-ranking/']
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 " \
                 "Safari/537.1 "

    def __init__(self, scope='one'):
        super().__init__(scope)
        self.scope = scope

    def parse(self, response, **kwargs):
        if self.scope == 'all':
            links = response.css('.entry-content li a ::attr(href)').getall()
        else:
            links = [response.css('.entry-content li a ::attr(href)').get()]

        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=parse_detail,
            )


def parse_detail(response):
    def peel_text(text):
        text = text.strip()
        value = text.split(':')[1].strip()
        return value

    contentSection = response.css('.entry-content')

    # The middle column of table, where base stats and other stuff are presented.
    propertySection = contentSection.xpath('./table//tr/td[2]')

    # info attributes (faction / affinity and etc.
    sectionInfoAttr = propertySection.xpath('./p[1]')
    attr = dict(
        faction=sectionInfoAttr.xpath('./a[1]/text()').get(),
        rarity=sectionInfoAttr.xpath('./a[2]/text()').get(),
        role=sectionInfoAttr.xpath('./a[3]/text()').get(),
        affinity=sectionInfoAttr.xpath('./a[4]/text()').get(),
        usability=peel_text(sectionInfoAttr.xpath('./br[4]/following-sibling::text()').get()),
        books=peel_text(sectionInfoAttr.xpath('./br[5]/following-sibling::text()').get()),
    )

    # base stats
    sectionInfoStats = propertySection.xpath('./p[2]')
    stats = dict(
        stats_hp=peel_text(sectionInfoStats.xpath('./text()[1]').get()),
        stats_atk=peel_text(sectionInfoStats.xpath('./text()[2]').get()),
        stats_def=peel_text(sectionInfoStats.xpath('./text()[3]').get()),
        stats_spd=peel_text(sectionInfoStats.xpath('./text()[4]').get()),
        stats_crate=peel_text(sectionInfoStats.xpath('./text()[5]').get()),
        stats_cdmg=peel_text(sectionInfoStats.xpath('./text()[6]').get()),
        stats_resist=peel_text(sectionInfoStats.xpath('./text()[7]').get()),
        stats_acc=peel_text(sectionInfoStats.xpath('./text()[8]').get()),
    )

    yield {
        'attributes': attr,
        'stats': stats,
    }
