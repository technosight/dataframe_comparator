from unittest import TestCase
from df_comparator import DfComparator
from pathlib import Path
import pandas as pd

class TestDfComparator(TestCase):

    def setUp(self):
        data_folder = Path(__file__).resolve().parent.parent / 'data'
        # files = data_folder.glob('*.csv')
        # print(files)
        self.left_df = pd.read_csv(data_folder / 'teams_left.csv', sep=',')
        self.right_df_identical = pd.read_csv(data_folder / 'teams_right_identical.csv', sep=',')
        self.right_df_modified = pd.read_csv(data_folder / 'teams_right_modified.csv', sep=',')

    def test_compare(self):
        comparator = DfComparator()

        result_df_1 = comparator.compare(self.left_df, self.right_df_identical)
        self.assertTrue(result_df_1.size == 0)

        result_df_2 = comparator.compare(self.left_df, self.right_df_modified)
        self.assertTrue(result_df_2.size == 6)
