from django.shortcuts import render
from django.template.response import TemplateResponse
from collector.models import billInfo, billAcceptInfo

import bs4
import requests
import datetime

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

    contents = data.findAll("div", attrs={"class": "contIn"})

    # contIn div 아래 subti h5가 분류 결정
    # contIn div 안에 테이블에서 데이터 추출
    billnum = ""
    for cont in contents:
        type = cont.find("h5", attrs={"class": "subti02"}).text
        type = type.replace("▶ ", "")

        div = cont.find("div", attrs={"class": "tableCol01"})
        tbody = div.find("tbody")
        tr = tbody.find("tr")
        tds = tr.findAll("td")

        if type == "의안접수정보":            
            billnum = tds[0].text
            billProposeDate = tds[1].text
            billProposeDate = datetime.datetime.strptime(billProposeDate, "%Y-%m-%d")
            billProposer = tds[2].text.strip()

            billAcceptInfo.objects.create(
                bill=billInfo.objects.get(billNum=billnum),
                process=process,
                proposeDate=billProposeDate,
                proposer=billProposer
            )
        elif type == "소관위 심사정보":
            committee = tds[0].text.split()
            sendingDate = tds[1].text
            introDate = tds[2].text
            disposeDate = tds[3].text
            disposeResult = tds[4].text.split()

            print(committee)
            print(sendingDate)
            print(introDate)
            print(disposeResult)
            print(disposeDate)





