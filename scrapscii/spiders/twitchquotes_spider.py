import scrapy

import scrapscii.unicode

# COPYPASTA ####################################################################

class TwitchQuotesSpider(scrapy.Spider):
    name = "twitchquotes"

    def start_requests(self):
        __urls = [
            f'https://www.twitchquotes.com/copypastas/ascii-art?page={__i}'
            for __i in range(1, 54)]
        for __u in __urls:
            yield scrapy.Request(url=__u, callback=self.parse)

    def parse(self, response):
        for __pasta in response.css('article.twitch-copypasta-card'):
            # parse
            __caption = __pasta.css('h3.-title-inner-parent::text').get()
            __content = __pasta.css('span.-main-text::text').get()
            # format
            if __caption and __content:
                yield {
                    'caption': __caption,
                    'content': __content,
                    'charsets': ','.join(set(scrapscii.unicode.lookup_section(__c) for __c in __content)),
                    'chartypes': ','.join(set(scrapscii.unicode.lookup_category(__c) for __c in __content)),}
