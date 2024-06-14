import pandas as pd

from pysankey.sankey import _create_dataframe
from tests.generic_test import TestCustomerGood


class TestCreateDataframeCustomerGood(TestCustomerGood):
    """Tests the create_dataframe function on the data in customers-goods.csv"""

    def test_dataframe_correct_type(self) -> None:
        dataframe = _create_dataframe(
            left=self.data["customer"],
            leftWeight=self.data["revenue"],
            right=self.data["good"],
            rightWeight=self.data["revenue"],
        )
        self.assertIsInstance(dataframe, pd.DataFrame)

    def test_sorted_dataframe(self) -> None:
        """
        Tests that if we pass a sorted dataframe, it doesn't change the values due to
        an index mismatch.
        """
        # Pass the data as is
        dataframe = _create_dataframe(
            left=self.data["customer"],
            leftWeight=self.data["revenue"],
            right=self.data["good"],
            rightWeight=self.data["revenue"],
        )

        # Now pass a sorted dataframe in
        data_sorted = self.data.sort_values(by="revenue").copy()
        dataframe_sorted = _create_dataframe(
            left=data_sorted["customer"],
            leftWeight=data_sorted["revenue"],
            right=data_sorted["good"],
            rightWeight=data_sorted["revenue"],
        )

        # Check that the values are still the same if we sort both dataframes
        # the same way
        assert (
            dataframe.sort_values(by="leftWeight").values == dataframe_sorted.values
        ).all()
