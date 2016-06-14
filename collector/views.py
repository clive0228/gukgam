from django.shortcuts import render
from collector.models import billInfo
from django.template.response import TemplateResponse

import bs4
import requests

def list_collector(request):

    bills = billInfo.objects.all()
    context = {'bills': bills}

    return TemplateResponse(request, 'index.html', context)

# get basic information for each bills.
def bill_url_collector(agefrom, ageto, pagesize, maxpage):
    r = requests.Session()
    r.headers.update({'referer': 'http://likms.assembly.go.kr/bill/main.do'})
    front_url = 'http://likms.assembly.go.kr/bill/billDetail.do?billId='

    for page in range(1, maxpage + 1): # to end of the pages
        data = r.get(
            'http://likms.assembly.go.kr/bill/BillSearchResult.do?ageFrom=' + str(agefrom)
            + '&ageTo=' + str(ageto) + '&pageSize=' + str(pagesize) + '&strPage=' + str(page)
        ) # ageForm -> 회기시작, ageTo -> 회기종료, pageSize -> 페이지당 의안 수, strPage -> 확인할 페이지 
        data = data.text.encode(data.encoding)
        data = bs4.BeautifulSoup(data)

        table = data.find("div", attrs={'class': 'tableCol01'})
        trs = table.findAll('tr')

        for tr in trs[1:]:
            tds = tr.findAll('td')
            link = tds[1].find('a').get('href')
            name = tds[1].text
            num = tds[0].text
            link = front_url + link.replace('javascript:fGoDetail(\'', '').replace('\', \'\')', '')
            try:
                billInfo.objects.create(billNum=num, billName=name, billUrl=link)
            except:
                pass

        print("####### page" + str(page) + " complete #######")
        print("current number of objects: " + str(billInfo.objects.count()))

def bill_detail(info):
    r = requests.Session()
    r.headers.update({'referer': 'http://likms.assembly.go.kr/bill/BillSearchResult.do'})

    data = r.get(info.billUrl)
    data = data.text.encode(data.encoding)
    data = bs4.BeautifulSoup(data)

    process = data.find("span", attrs={"class": "on"}).text

    cotents = data.findAll("div", attrs={"class": "contIn"})

    # contIn div 아래 subti h5가 분류 결정
    # contIn div 안에 테이블에서 데이터 추출
    billnum = ""
    for cont in contents:
        type = cont.find("h5", attrs={"class": "subti01"}).text

        if type == "의안접수정보":
            tbody = cont.find("tbody")
            tr = cont.find("tr")
            tds = tr.find("td")
            billnum = td[0].text
            billProposeDate = td[1].text
            billProposer = td[2].text





