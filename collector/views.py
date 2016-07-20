from django.shortcuts import render
from django.template.response import TemplateResponse
from collector.models import (
    billInfo, billAcceptInfo, JurisJudgeInfo, JurisConfInfo, LegisJudgeInfo,
    LegisConfInfo, MainConfInfo, TransferInfo, ProclaimInfo, RelJudgeInfo, AdditionalInfo
)
from concurrent.futures import ThreadPoolExecutor

import bs4
import requests
import datetime

def list_collector(request):
    # bill_url_collector(19, 19, 100, 190)

    bills = billInfo.objects.all()
    # SCREEN_CODE = "\033[1A[\033[2K"
    # with ThreadPoolExecutor(max_workers=10) as executor:
        # for bill in bills:
            # rate = str((billAcceptInfo.objects.count() / 18926) * 100)
            # print("Complete " + rate + "%")
            # executor.submit(bill_detail, bill)

    # print("done")
    # bai = billAcceptInfo.objects.all()
    # for ba in bai:
    #     print(ba.process)
    #     print(ba.proposeDate)
    #     print(ba.proposer)
    # return
    print(billInfo.objects.count())
    print(billAcceptInfo.objects.count())
    print(JurisJudgeInfo.objects.count())
    print(JurisConfInfo.objects.count())
    print(LegisJudgeInfo.objects.count())
    print(LegisConfInfo.objects.count())
    print(MainConfInfo.objects.count())
    print(TransferInfo.objects.count())
    print(ProclaimInfo.objects.count())
    print(RelJudgeInfo.objects.count())
    print(AdditionalInfo.objects.count())

    # return
    context = {'bills': bills}

    with open("19th.csv", "w") as f:
        for bill in bills:
            print(bill.billName)
            f.write(bill.billNum + "," + bill.billName+ "," + bill.billUrl + ",")
            try:
                bai = billAcceptInfo.objects.filter(bill=bill)[0]
                f.write(bai.process + "," + bai.proposeDate.strftime("%Y-%m-%d") + "," + bai.proposer + ",")
            except:
                f.write(",,,")
            try:
                jji = JurisJudgeInfo.objects.filter(bill=bill)[0]
                f.write(jji.committee + "," + jji.sendingDate.strftime("%Y-%m-%d") + "," + jji.introDate.strftime("%Y-%m-%d") + "," + jji.disposeDate.strftime("%Y-%m-%d") + "," +jji.disposeResult + ",")
            except:
                f.write(",,,,,")
            try:
                jci = JurisConfInfo.objects.filter(bill=bill)[0]
                f.write(jci.confName + "," + jci.confDate.strftime("%Y-%m-%d") + "," + jci.confResult + ",")
            except:
                f.write(",,,")
            try:
                rji = RelJudgeInfo.objects.filter(bill=bill)[0]
                f.write(rji.relName + "," + rji.sendingDate.strftime("%Y-%m-%d") + "," + rji.introDate.strftime("%Y-%m-%d") + "," + rji.proposeDate.strftime("%Y-%m-%d") + ",")
            except:
                f.write(",,,,")
            try:
                lji = LegisJudgeInfo.objects.filter(bill=bill)[0]
                f.write(lji.sendingDate.strftime("%Y-%m-%d") + "," + lji.introDate.strftime("%Y-%m-%d") + "," + lji.disposeDate.strftime("%Y-%m-%d") + "," + lji.disposeResult + ",")
            except:
                f.write(",,,,")
            try:
                lci = LegisConfInfo.objects.filter(bill=bill)[0]
                f.write(lci.confName + "," + lci.confDate.strftime("%Y-%m-%d") + "," + lci.confResult + ",")
            except:
                f.write(",,,")
            try:
                mci = MainConfInfo.objects.filter(bill=bill)[0]
                f.write(mci.introDate.strftime("%Y-%m-%d") + "," + mci.decisionDate.strftime("%Y-%m-%d") + "," + mci.confName + "," + mci.confResult + ",")
            except:
                f.write(",,,,")
            try:
                ti = TransferInfo.objects.filter(bill=bill)[0]
                f.write(ti.transferDate.strftime("%Y-%m-%d") + ",")
            except:
                f.write(",")
            try:                
                pi = ProclaimInfo.objects.filter(bill=bill)[0]
                f.write(pi.proclaimDate.strftime("%Y-%m-%d") + "," + pi.proclaimNum + "," + pi.proclaimLaw + ",")
            except:
                f.write(",,,")
            try:
                ais = AdditionalInfo.objects.filter(bill=bill)
                for ai in ais:
                    if ai.type == 1:
                        f.write("대안:")
                    elif ai.type == 2:
                        f.write("비고:")
                    elif ai.type == 3:
                        f.write("타법정보:")
                    f.write(ai.content.strip().replace("\t", "").replace("\n", ""))
            except:
                f.write("")
            f.write("\n")

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
            name = tds[1].text.strip().replace(",", ".")
            num = tds[0].text
            link = front_url + link.replace('javascript:fGoDetail(\'', '').replace('\', \'\')', '')
            try:
                billInfo.objects.create(billNum=num, billName=name, billUrl=link)
            except:
                pass

        print("####### page" + str(page) + " complete #######")
        print("current number of objects: " + str(billInfo.objects.count()))

# get detail informations for each bills.
def bill_detail(info):
    r = requests.Session()
    r.headers.update({'referer': 'http://likms.assembly.go.kr/bill/BillSearchResult.do'})

    data = r.get(info.billUrl)
    print(info.billNum)
    data = data.text.encode(data.encoding)
    data = bs4.BeautifulSoup(data)

    # 의안처리 진행단계
    process = data.find("span", attrs={"class": "on"}).text

    contents = data.findAll("div", attrs={"class": "contIn"})

    # contIn div 아래 subti02 h5가 분류 결정
    # contIn div 안에 테이블에서 데이터 추출
    # 한개의 contIn div 안에 여러개의 subti02일 경우 관련위 혹은 법사위
    billnum = ""
    for cont in contents:
        titles = cont.findAll("h5", attrs={"class": "subti02"})
        titles = [title.text.replace("▶ ", "") for title in titles]
        
        try:
            div = cont.find("div", attrs={"class": "tableCol01"})
            tbody = div.find("tbody")
            tr = tbody.find("tr")
            tds = tr.findAll("td")
        except:
            try:
                cont.find("div", attrs={"class": "TEXTTYPE02"})
            except:
                continue

        for type in titles:
            if type == "의안접수정보":            
                billnum = tds[0].text
                billProposeDate = tds[1].text.strip()
                billProposer = tds[2].text.strip()

                billAcceptInfo.objects.create(
                    bill=billInfo.objects.get(billNum=billnum),
                    process=process,
                    proposeDate=billProposeDate,
                    proposer=billProposer
                )
                # print("의안접수")
            elif type == "소관위 심사정보":
                committee = tds[0].text.strip().replace(",", ".")
                sendingDate = tds[1].text.strip()
                introDate = tds[2].text.strip()
                disposeDate = tds[3].text.strip()
                disposeResult = tds[4].text.strip()

                if sendingDate == '':
                    sendingDate = '1900-01-01'
                if introDate == '':
                    introDate = '1900-01-01'
                if disposeDate == '':
                    disposeDate = '1900-01-01'

                JurisJudgeInfo.objects.create(
                    bill=billInfo.objects.get(billNum=billnum),
                    committee=committee,
                    sendingDate=sendingDate,
                    introDate=introDate,
                    disposeDate=disposeDate,
                    disposeResult=disposeResult
                )
                # print("소관위심사")

                if len(titles) > 1:
                    for title in titles[1:]:
                        if title == "소관위 회의정보":
                            table = cont.find("table", attrs={"summary": "소관위 회의정보"})
                            tbody = table.find("tbody")
                            tr = tbody.find("tr")
                            tds = tr.findAll("td")

                            confName = tds[0].text.strip()
                            confDate = tds[1].text.strip()
                            confResult = tds[2].text.strip()

                            if confDate == '':
                                confDate = '1900-01-01'

                            JurisConfInfo.objects.create(
                                bill=billInfo.objects.get(billNum=billnum),
                                confName=confName,
                                confDate=confDate,
                                confResult=confResult
                            )
                            # print("소관위회의")
                        elif title == "법사위 체계자구심사정보":
                            table = cont.find("table", attrs={"summary": "법사위 체계자구심사정보"})
                            tbody = table.find("tbody")
                            tr = tbody.find("tr")
                            tds = tr.findAll("td")

                            sendingDate = tds[0].text.strip()
                            introDate = tds[1].text.strip()
                            disposeDate = tds[2].text.strip()
                            disposeResult = tds[3].text.strip()

                            if sendingDate == '':
                                sendingDate = '1900-01-01'
                            if introDate == '':
                                introDate = '1900-01-01'
                            if disposeDate == '':
                                disposeDate = '1900-01-01'

                            LegisJudgeInfo.objects.create(
                                bill=billInfo.objects.get(billNum=billnum),
                                sendingDate=sendingDate,
                                introDate=introDate,
                                disposeDate=disposeDate,
                                disposeResult=disposeResult
                            )
                            # print("법사위심사")
                        elif title == "법사위 회의정보":
                            table = cont.find("table", attrs={"summary": "법사위 회의정보"})
                            tbody = table.find("tbody")
                            tr = tbody.find("tr")
                            tds = tr.findAll("td")

                            confName = tds[0].text.strip()
                            confDate = tds[1].text.strip()
                            confResult = tds[2].text.strip()

                            if confDate == '':
                                confDate = '1900-01-01'

                            LegisConfInfo.objects.create(
                                bill=billInfo.objects.get(billNum=billnum),
                                confName=confName,
                                confDate=confDate,
                                confResult=confResult
                            )
                            # print("법사위회의")
                        elif title == "관련위 심사정보":
                            table = cont.find("table", attrs={"summary": "관련위 심사정보"})
                            tbody = table.find("tbody")
                            trs = tbody.findAll("tr")

                            for tr in trs:
                                tds = tr.findAll("td")
                                relName = tds[0].text.strip()
                                sendingDate = tds[1].text.strip()
                                introDate = tds[2].text.strip()
                                proposeDate = tds[3].text.strip()

                                RelJudgeInfo.objects.create(
                                    bill=billInfo.objects.get(billNum=billnum),
                                    relName=relName,
                                    sendingDate=sendingDate,
                                    introDate=introDate,
                                    proposeDate=proposeDate
                                )

                            # print("관련위심사")
            elif type == "본회의 심의정보":
                introDate = tds[0].text.strip()
                decisionDate = tds[1].text.strip()
                confName = tds[2].text.strip()
                confResult = tds[3].text.strip()

                if introDate == "":
                    introDate = "1900-01-01"
                if decisionDate == "":
                    decisionDate = "1900-01-01"

                MainConfInfo.objects.create(
                    bill=billInfo.objects.get(billNum=billnum),
                    introDate=introDate,
                    decisionDate=decisionDate,
                    confName=confName,
                    confResult=confResult
                )
                # print("본회의")
            elif type == "정부이송정보":
                transferDate = tds[0].text.strip()
                if transferDate == "":
                    transferDate = '1900-01-01'

                t = TransferInfo.objects.create(
                    bill=billInfo.objects.get(billNum=billnum),
                    transferDate=transferDate
                )
                # print("정부이송")
            elif type == "공포정보":
                proclaimDate = tds[0].text.strip()
                proclaimNum = tds[1].text.strip()
                proclaimLaw = tds[2].text.strip()

                if proclaimDate == "":
                    proclaimDate = "1900-01-01"

                ProclaimInfo.objects.create(
                    bill=billInfo.objects.get(billNum=billnum),
                    proclaimDate=proclaimDate,
                    proclaimNum=proclaimNum,
                    proclaimLaw=proclaimLaw
                )
                # print("공포")
            elif "대안반영폐기 의안목록" in type:
                additional = cont.find("div", attrs={"class": "TEXTTYPE02"})
                ps = additional.findAll("p")
                for p in ps:
                    a = p.find("a")
                    AdditionalInfo.objects.create(
                        bill=billInfo.objects.get(billNum=billnum),
                        content=a.text,
                        type=1
                    )
                # print("대안")
            elif type == "비고":
                additional = cont.find("div", attrs={"class": "TEXTTYPE02"})
                AdditionalInfo.objects.create(
                    bill=billInfo.objects.get(billNum=billnum),
                    content=additional.text.strip(),
                    type=2
                )
                # print("비고")
            elif type == "타법정보":
                additional = cont.find("div", attrs={"class": "TEXTTYPE02"})
                ps = additional.findAll("p")
                for p in ps:
                    atags = p.findAll("a")
                    for a in atags:
                        AdditionalInfo.objects.create(
                            bill=billInfo.objects.get(billNum=billnum),
                            content=a.text,
                            type=3
                        )
                # print("타법")



            
            


