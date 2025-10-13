import scrapy

class BooliSpider(scrapy.Spider):
    name = 'katla'
    start_urls = [
                  f'https://www.booli.se/sok/slutpriser?areaIds=106602'
                  for i in range(1, 5)
    ]

    def parse(self, response):
        for listings in response.css('div.object-card-layout.object-card-layout--default'):
            name = listings.css(
                'a.expanded-link::text'
            ).get()

            if not name:
                continue # Skip if no name present

            price_str = listings.css(
                'div.object-card__price-container span.object-card__price__logo::text'
            ).get()

            date_str = listings.css(
                'span.object-card__date__logo::text'
            ).get()

            # Price increase relative to the starting price
            price_increase = (
                listings.css(
                    'div.heading-4::text'
                ).get()
                or listings.css(
                    'div.object-card__price-trend span::text'
                ).get()
            )

            # Convert to integer
            if price_str:
                final_price = int(''.join(filter(str.isdigit, price_str)))
            else:
                final_price = None # Fallback if price not found

            yield {
                'name': name,
                'final_price': final_price,
                'date_str': date_str,
                'price_increase': price_increase
            }