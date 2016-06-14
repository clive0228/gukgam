from django.test import TestCase
from collector.views import bill_detail
from collector.models import billInfo, billAcceptInfo

class CollectorTest(TestCase):

    def test_can_collect_bill_accept_info(self):
        bill = billInfo.objects.create(
            billNum=1918135,
            billName="박근혜 대통령 탄핵소추안",
            billUrl="http://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_J1K5F1Y1H2Y7U1P7I4A0X3C5O4X9F8"
        )
        bill_detail(bill)