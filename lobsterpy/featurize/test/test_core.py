import os
import sys
import unittest
import pandas as pd
from pathlib import Path
from lobsterpy.featurize.core import FeaturizeLobsterpy

CurrentDir = Path(__file__).absolute().parent
TestDir = CurrentDir / "../../"


class TestFeaturizeLobsterpy(unittest.TestCase):
    def setUp(self):
        self.featurize_mp1249_json = FeaturizeLobsterpy(
            path_to_json=TestDir / "TestData/JSONS/mp-1249.json.gz", bonds="all_bonds"
        )
        self.featurize_mp1958_json = FeaturizeLobsterpy(
            path_to_json=TestDir / "TestData/JSONS/mp-1958.json.gz", bonds="all_bonds"
        )
        self.featurize_mp14652_json = FeaturizeLobsterpy(
            path_to_json=TestDir / "TestData/JSONS/mp-14652.json.gz", bonds="all_bonds"
        )

    def test_featurize_mp1249_json(self):
        df = self.featurize_mp1249_json.get_df(ids="mp-1249")

        # Test that the function returns a pandas DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Test that the DataFrame has the expected columns
        expected_cols = [
            "Icohp_mean_avg",
            "Icohp_mean_max",
            "Icohp_mean_min",
            "Icohp_mean_std",
            "Icohp_sum_avg",
            "Icohp_sum_max",
            "Icohp_sum_min",
            "Icohp_sum_std",
            "bonding_perc_avg",
            "bonding_perc_max",
            "bonding_perc_min",
            "bonding_perc_std",
            "antibonding_perc_avg",
            "antibonding_perc_min",
            "antibonding_perc_max",
            "antibonding_perc_std",
            "Madelung_Mull",
            "Madelung_Loew",
        ]
        self.assertCountEqual(list(df.columns), expected_cols)

        # Test that the DataFrame has the expected index
        self.assertEqual(df.index[0], "mp-1249")

        # Test that all the values in the DataFrame
        self.assertAlmostEqual(df.loc["mp-1249", "Icohp_mean_avg"], -1.020000, places=5)
        self.assertAlmostEqual(df.loc["mp-1249", "Icohp_mean_max"], -1.020000, places=5)
        self.assertAlmostEqual(df.loc["mp-1249", "Icohp_mean_min"], -1.020000, places=5)
        self.assertAlmostEqual(df.loc["mp-1249", "Icohp_mean_std"], 0.000000, places=5)
        self.assertAlmostEqual(df.loc["mp-1249", "Madelung_Mull"], -52.000000, places=5)
        self.assertAlmostEqual(
            df.loc["mp-1249", "bonding_perc_avg"], 0.978985, places=5
        )

    def test_featurize_mp1958_json(self):
        df = self.featurize_mp1958_json.get_df(ids="mp-1958")

        # Test that the function returns a pandas DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Test that the DataFrame has the expected columns
        expected_cols = [
            "Icohp_mean_avg",
            "Icohp_mean_max",
            "Icohp_mean_min",
            "Icohp_mean_std",
            "Icohp_sum_avg",
            "Icohp_sum_max",
            "Icohp_sum_min",
            "Icohp_sum_std",
            "bonding_perc_avg",
            "bonding_perc_max",
            "bonding_perc_min",
            "bonding_perc_std",
            "antibonding_perc_avg",
            "antibonding_perc_min",
            "antibonding_perc_max",
            "antibonding_perc_std",
            "Madelung_Mull",
            "Madelung_Loew",
        ]
        self.assertCountEqual(list(df.columns), expected_cols)

        # Test that the DataFrame has the expected index
        self.assertEqual(df.index[0], "mp-1958")

        # Test that all the values in the DataFrame
        self.assertAlmostEqual(df.loc["mp-1958", "Icohp_sum_avg"], -2.96000, places=5)
        self.assertAlmostEqual(df.loc["mp-1958", "Icohp_sum_max"], -2.96000, places=5)
        self.assertAlmostEqual(df.loc["mp-1958", "Icohp_sum_min"], -2.96000, places=5)
        self.assertAlmostEqual(df.loc["mp-1958", "Icohp_sum_std"], 0.000000, places=5)
        self.assertAlmostEqual(df.loc["mp-1958", "Madelung_Loew"], -16.68000, places=5)
        self.assertAlmostEqual(
            df.loc["mp-1958", "antibonding_perc_avg"], 0.14528, places=5
        )

    def test_featurize_mp14652_json(self):
        df = self.featurize_mp14652_json.get_df(ids="mp-14652")

        # Test that the function returns a pandas DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Test that the DataFrame has the expected columns
        expected_cols = [
            "Icohp_mean_avg",
            "Icohp_mean_max",
            "Icohp_mean_min",
            "Icohp_mean_std",
            "Icohp_sum_avg",
            "Icohp_sum_max",
            "Icohp_sum_min",
            "Icohp_sum_std",
            "bonding_perc_avg",
            "bonding_perc_max",
            "bonding_perc_min",
            "bonding_perc_std",
            "antibonding_perc_avg",
            "antibonding_perc_min",
            "antibonding_perc_max",
            "antibonding_perc_std",
            "Madelung_Mull",
            "Madelung_Loew",
        ]
        self.assertCountEqual(list(df.columns), expected_cols)

        # Test that the DataFrame has the expected index
        self.assertEqual(df.index[0], "mp-14652")

        # Test that all the values in the DataFrame
        self.assertAlmostEqual(df.loc["mp-14652", "Icohp_mean_std"], 2.335070, places=5)
        self.assertAlmostEqual(
            df.loc["mp-14652", "bonding_perc_max"], 0.889620, places=5
        )
        self.assertAlmostEqual(
            df.loc["mp-14652", "bonding_perc_min"], 0.873420, places=5
        )
        self.assertAlmostEqual(
            df.loc["mp-14652", "bonding_perc_std"], 0.006339, places=5
        )
        self.assertAlmostEqual(
            df.loc["mp-14652", "antibonding_perc_min"], 0.110380, places=5
        )
        self.assertAlmostEqual(
            df.loc["mp-14652", "antibonding_perc_max"], 0.126580, places=5
        )
        self.assertAlmostEqual(
            df.loc["mp-14652", "antibonding_perc_std"], 0.006339, places=5
        )


if __name__ == "__main__":
    unittest.main()
