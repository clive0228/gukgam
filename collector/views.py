from django.shortcuts import render
from collector.models import billInfo
from django.template.response import TemplateResponse

import bs4
import requests

def list_collector(request):
    r = requests.Session()
    r.headers.update({'referer': 'http://likms.assembly.go.kr/bill/main.do'})
    front_url = 'http://likms.assembly.go.kr/bill/billDetail.do?billId='

    # for page in range(1, 191):
    #     data = r.get(
    #         'http://likms.assembly.go.kr/bill/BillSearchResult.do?ageFrom=19&ageTo=19&pageSize=100&strPage='+str(page)
    #     )
    #     data = data.text.encode(data.encoding)
    #     data = bs4.BeautifulSoup(data)

    #     table = data.find("div", attrs={'class': 'tableCol01'})
    #     trs = table.findAll('tr')

    #     for tr in trs[1:]:
    #         tds = tr.findAll('td')
    #         link = tds[1].find('a').get('href')
    #         name = tds[1].text
    #         num = tds[0].text
    #         link = front_url + link.replace('javascript:fGoDetail(\'', '').replace('\', \'\')', '')
    #         try:
    #             billInfo.objects.create(billNum=num, billName=name, billUrl=link)
    #         except:
    #             pass
    #     print("####### page" + str(page) + " complete #######")
    #     print("current number of objects: " + str(billInfo.objects.count()))

    bills = billInfo.objects.all()
    context = {'bills': bills}

    return TemplateResponse(request, 'index.html', context)

def bill_detail(info):
    r = requests.Session()
    r.headers.update({'referer': 'http://likms.assembly.go.kr/bill/BillSearchResult.do'})

    data = r.get(info.billUrl)
    data = data.text.encode(data.encoding)
    data = bs4.BeautifulSoup(data)

