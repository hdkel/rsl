from abc import ABC
import scrapy
from url_source import URLSource
from source.source_ayumilove_stats import SourceAyumiLoveStats
from source.source_ayumilove_ranking import SourceAyumiLoveRanking


# Usage: scrapy runspider scraper.py -a scope=random|all
class ShadowLegendsDataSpider(scrapy.Spider, ABC):

    urls = ['']
    name = "shadow_legends_data_spider"
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1217.1 " \
                 "Safari/537.1 "
    start_urls = [
        URLSource.AYUMI_LOVE_STATS.value,
        URLSource.AYUMI_LOVE_RANKING.value,
    ]

    def __init__(self, scope='random'):
        super().__init__(scope)
        self.scope = scope

    def start_requests(self):
        for url in self.start_urls:
            if url == URLSource.AYUMI_LOVE_STATS.value:
                yield scrapy.Request(
                    url,
                    callback=SourceAyumiLoveStats().parse,
                    cb_kwargs=dict(scope=self.scope),
                )
            elif url == URLSource.AYUMI_LOVE_RANKING.value:
                yield scrapy.Request(
                    url,
                    callback=SourceAyumiLoveRanking().parse,
                    cb_kwargs=dict(scope=self.scope),
                )
