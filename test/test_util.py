from unittest import TestCase
from util import util


class Test(TestCase):
    def test_make_date(self):
        a = util.makeDate(2020, 1, 1)
        m = 0


