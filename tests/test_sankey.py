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

    def test_fontfamily_parameter(self) -> None:
        """Test that fontfamily parameter works and doesn't break existing functionality"""
        # Test with default fontfamily (serif)
        ax1 = sankey(self.data["true"], self.data["predicted"])
        self.assertIsInstance(ax1, plt.Axes)
        
        # Test with sans-serif fontfamily
        ax2 = sankey(self.data["true"], self.data["predicted"], fontfamily="sans-serif")
        self.assertIsInstance(ax2, plt.Axes)
        
        # Test with monospace fontfamily
        ax3 = sankey(self.data["true"], self.data["predicted"], fontfamily="monospace")
        self.assertIsInstance(ax3, plt.Axes)
