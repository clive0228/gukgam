from django.test import TestCase
from collector.views import bill_detail
from collector.models import billInfo, billAcceptInfo

class CollectorTest(TestCase):

    def test_can_collect_bill_accept_info(self):
        bill = billInfo.objects.create(
            billNum=1918538,
            billName="박근혜 대통령 탄핵소추안",
            billUrl="http://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_Z1B6Z0F2E0K4Z1D7G2B9Q2F0U1K0Q9"
        )
        bill_detail(bill)