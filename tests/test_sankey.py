import matplotlib.pyplot as plt
from pysankey import sankey

from tests.generic_test import TestFruit


class TestSankey(TestFruit):
    def test_right_color(self) -> None:
        ax = sankey(self.data["true"], self.data["predicted"], rightColor=True)
        self.assertIsInstance(ax, plt.Axes)

    def test_single(self) -> None:
        source = [1]
        target = [2]
        sankey(source, target, rightColor=True)
