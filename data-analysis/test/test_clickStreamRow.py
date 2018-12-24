from unittest import TestCase

from model.clickstream import ClickStreamRow, normalise_cs_line


class TestClickStreamRow(TestCase):

    def setUp(self):
        super().setUp()
        header_v1 = '"Search_Term","PPID_Clicked","Total_Times_Clicked",' \
                    '"Total_Times_AddToBag","Total_Times_Checked_Out","Total_Search_Count"'
        line_v1 = '"red jeans","pp1110","1",,,"10"'
        self.test_line_v1 = ClickStreamRow(normalise_cs_line(line_v1), header_v1)

    def test_new_v1_row(self):
        self.assertEqual(self.test_line_v1.phrase, 'red jeans')
        self.assertEqual(self.test_line_v1.product, 'pp1110')
        self.assertEqual(self.test_line_v1.impr, 10)
        self.assertEqual(self.test_line_v1.clicks, 1)
        self.assertEqual(self.test_line_v1.add_to_cart, 0)
        self.assertEqual(self.test_line_v1.checked_out, 0)

    def test_new_v2_row(self):
        header_v2 = 'Search_Term,PPID_Clicked,Total_Search_Count,Total_Times_Clicked,' \
                    'Total_Times_AddToBag,Total_Times_Checked_Out'
        line_v2 = 'red jeans,1110,200,1,0,0'
        test_line_v2 = ClickStreamRow.new_v2_row(line_v2, header_v2)
        self.assertEqual(test_line_v2.phrase, 'red jeans')
        self.assertEqual(test_line_v2.product, '1110')
        self.assertEqual(test_line_v2.impr, 200)
        self.assertEqual(test_line_v2.clicks, 1)
        self.assertEqual(test_line_v2.add_to_cart, 0)
        self.assertEqual(test_line_v2.checked_out, 0)

    def test_get_clicks_data_as_dict(self):
        line_dict = {
            'search_count_value': 10,
            'clicked_value': 1,
            'add_to_bag_value': 0,
            'checked_out_value': 0
        }
        self.assertEqual(self.test_line_v1.get_clicks_data_as_dict(), line_dict)
