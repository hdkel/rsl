import scrapy
import random
import json


class SourceAyumiLoveStats:

    # parse defines the rules to parse the index page, in order to get URLs to all detail pages
    # @see https://ayumilove.net/raid-shadow-legends-list-of-champions-by-ranking/ for DOM structure
    def parse(self, response, scope='random'):

        links = response.css('.entry-content li a ::attr(href)').getall()
        links_to_crawl = []

        if scope == 'all':
            links_to_crawl = links
        elif scope == 'random':
            rnd = random.randrange(len(links) - 1)
            links_to_crawl = [links[rnd]]

        for link in links_to_crawl:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_detail,
            )

    # parse_detail defines the rules to parse data from a detail page
    # @see https://ayumilove.net/raid-shadow-legends-krisk-the-ageless-skill-mastery-equip-guide/ for DOM structure
    def parse_detail(self, response):

        def peel_text(text, splitter=':', part_idx=1):
            text = text.strip()
            value = text.split(splitter)[part_idx].strip()
            return value

        # Grab name (as unique identifier) from header
        headerSection = response.css('.entry-header')
        name = peel_text(headerSection.xpath('./h1/text()').get(), '|', 0)

        # Stats
        contentSection = response.css('.entry-content')
        # The middle column of table, where base stats and other stuff are presented.
        propertySection = contentSection.xpath('./table//tr/td[2]')

        # info attributes (faction / affinity and etc.
        sectionInfoAttr = propertySection.xpath('./p[1]')
        book = peel_text(sectionInfoAttr.xpath('./br[5]/following-sibling::text()').get())
        attr = dict(
            faction=sectionInfoAttr.xpath('./a[1]/text()').get(),
            rarity=sectionInfoAttr.xpath('./a[2]/text()').get(),
            role=sectionInfoAttr.xpath('./a[3]/text()').get(),
            affinity=sectionInfoAttr.xpath('./a[4]/text()').get(),
            books_total=book.split(" ")[0]
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

        filename = f'results/stats-{name.lower().replace(" ", "-")}.json'
        with open(filename, 'wb') as f:
            f.write(json.dumps({
                'name': name,
                'attributes': attr,
                'stats': stats,
            }).encode())
