from unittest import TestCase
import unittest
from model import trainingset


class TestTrainingSetRow(TestCase):

    def setUp(self):
        super().setUp()
        header = '#0->on_sale 1->bm25_score'
        line = '2 qid:0 0:0 1:4.1 #red jeans->1120'
        self.test_row = trainingset.TrainingSetRow(line, header)

    def test_row_creation(self):
        self.assertEqual(self.test_row.query, 'red jeans')
        self.assertEqual(self.test_row.product_id, '1120')
        self.assertEqual(self.test_row.rank, 2)
        self.assertEqual(self.test_row.qid, 0)
        features_dict = {
            'on_sale': '0',
            'bm25_score': '4.1'
        }
        self.assertDictEqual(self.test_row.features, features_dict)

    def test_row_asDict(self):
        row_dict = {
            'on_sale': '0',
            'bm25_score': '4.1',
            'rank': 2,
            'query': 'red jeans',
            'product_id': '1120',
            'qid': 0
        }
        self.assertDictEqual(self.test_row.get_as_dict(), row_dict)

    def test_get_by_name(self):
        self.assertEqual(self.test_row.get('bm25_score'), '4.1')
        self.assertEqual(self.test_row.get('rank'), 2)


if __name__ == '__main__':
    unittest.main()
