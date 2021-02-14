import scrapy
import random
import json


class SourceAyumiLoveRanking:
    # Source constants
    area_campaign = 'Campaign'
    area_arena_def = 'Arena Defense'
    area_arena_off = 'Arena Offense'
    area_cb = 'Clan Boss'
    area_fw = 'Faction Wars'
    area_scroll = 'Minotaur’s Labyrinth'
    area_spider = 'Spider’s Den'
    area_fire_knight = 'Fire Knight’s Castle'
    area_dragon = 'Dragon’s Lair'
    area_ice_golem = 'Ice Golem’s Peak'
    area_void_keep = 'Void Keep'
    area_force_keep = 'Force Keep'
    area_spirit_keep = 'Spirit Keep'
    area_magic_keep = 'Magic Keep'
    area_dt_dragon = 'Magma Dragon'
    area_dt_nether = 'Nether Spider'
    area_dt_frost = 'Frost Spider'
    area_dt_scarab = 'Scarab King'
    char_star = '★'
    char_empty_star = '✰'

    # TODO: this needs to go to a shared folder
    area_map = dict()
    area_map[area_campaign] = 'c'
    area_map[area_campaign] = 'c'
    area_map[area_arena_def] = 'adef'
    area_map[area_arena_off] = 'aoff'
    area_map[area_cb] = 'cb'
    area_map[area_fw] = 'fwar'
    area_map[area_scroll] = 'mino'
    area_map[area_spider] = 'spider'
    area_map[area_dragon] = 'dragon'
    area_map[area_fire_knight] = 'fnight'
    area_map[area_ice_golem] = 'icegolem'
    area_map[area_void_keep] = 'void'
    area_map[area_force_keep] = 'force'
    area_map[area_spirit_keep] = 'spirit'
    area_map[area_magic_keep] = 'magic'

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

        # Follow links to crawl
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

        def count_star(needle, haystack):
            return haystack.count(needle)

        # Grab name (as unique identifier) from header
        headerSection = response.css('.entry-header')
        name = peel_text(headerSection.xpath('./h1/text()').get(), '|', 0)

        # Rankings
        # TODO: might be empty for some champions
        contentSection = response.css('.entry-content')

        # The middle column of table, where ayumilove book/usability are presented.
        propertySection = contentSection.xpath('./table//tr/td[2]')

        # Pre-define dict for Ayumilove-only properties
        ayumi = dict()
        sectionInfoAttr = propertySection.xpath('./p[1]')
        book = peel_text(sectionInfoAttr.xpath('./br[5]/following-sibling::text()').get())
        ayumi['books_priority'] = " ".join(book.split(" ")[1:])
        ayumi['usability'] = peel_text(sectionInfoAttr.xpath('./br[4]/following-sibling::text()').get())

        # the right column of table, where ayumilove rank (per area) is presented
        ayumiRankSection = contentSection.xpath('./table//tr/td[3]')
        ayumiRanksParagraph = ayumiRankSection.xpath('./p/text()').getall()
        area_rank = dict()
        for rankTexts in ayumiRanksParagraph:

            # Data here looks like `★✰✰✰✰ Campaign`
            rankText = rankTexts.strip()
            rankLocation = " ".join(rankText.split(" ")[1:])
            rankStars = rankText.split()[0]

            if rankLocation in self.area_map:
                area_rank[self.area_map[rankLocation]] = count_star(self.char_star, rankStars)
        ayumi['arena_rank'] = area_rank

        filename = f'results/ayumi-ranking-{name.lower().replace(" ", "-")}.json'
        with open(filename, 'wb') as f:
            f.write(json.dumps({
                'name': name,
                'ayumi_rank': ayumi,
        }).encode())
