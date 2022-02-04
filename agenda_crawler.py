import scrapy
from datetime import date, timedelta


class agenda_spider(scrapy.Spider):
    name = "agenda_spider"
    start_urls = ['https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/2019-01-01']

    start_date = date(2019, 1, 2) 
    end_date = date(2022, 1, 29)
    delta = end_date - start_date

    lista_de_datas = list()
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        lista_de_datas.append('https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/'+str(day))    

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        lista_compromissos = response.xpath('//*[@id="content-core"]/div/ul/li')

        if lista_compromissos:
            li_ordem = 1
            for compromisso in lista_compromissos:
                yield {
                    'data' : response.xpath('//*[@id="breadcrumbs-current"]/text()').extract(),
                    'hora_inicio' : response.xpath('//*[@id="content-core"]/div/ul/li['+str(li_ordem)+']/div/div[1]/div/time[1]/text()').extract(),
                    'hora_fim' : response.xpath('//*[@id="content-core"]/div/ul/li['+str(li_ordem)+']/div/div[1]/div/time[2]/text()').extract(),
                    'titulo_compromisso' : response.xpath('//*[@id="content-core"]/div/ul/li['+str(li_ordem)+']/div/div[2]/h2/text()').extract(),
                    'compromisso_local' : response.xpath('//*[@id="content-core"]/div/ul/li['+str(li_ordem)+']/div/div[2]/div/div[1]/text()').extract()
                }
                li_ordem+=1
        else:
            yield {
                'data' : response.xpath('//*[@id="breadcrumbs-current"]/text()').extract(),
                'titulo_compromisso' : response.xpath('//*[@id="content-core"]/div/div[5]/p/strong/text()').extract()
            }

        for data in agenda_spider().lista_de_datas:
            yield response.follow(data, callback=self.parse)