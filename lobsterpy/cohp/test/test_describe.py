import os
import unittest

from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description

#TODO: Add example without antibonding states

class TestDescribe(unittest.TestCase):

    def setUp(self):
        self.analyse_NaCl = Analysis(path_to_poscar="TestData/NaCl/POSCAR",
                                     path_to_cohpcar="TestData/NaCl/COHPCAR.lobster",
                                     path_to_icohplist="TestData/NaCl/ICOHPLIST.lobster",
                                     path_to_charge="TestData/NaCl/CHARGE.lobster", whichbonds="cation-anion", \
                                     cutoff_icohp=0.1)
        self.describe_NaCl = Description(self.analyse_NaCl)


        self.analyse_NaCl_valences = Analysis(path_to_poscar="TestData/NaCl/POSCAR",
                                              path_to_cohpcar="TestData/NaCl/COHPCAR.lobster",
                                              path_to_icohplist="TestData/NaCl/ICOHPLIST.lobster",
                                              path_to_charge=None, whichbonds="cation-anion", \
                                              cutoff_icohp=0.1)
        self.describe_NaCl_valences = Description(self.analyse_NaCl_valences)

        self.analyse_BaTiO3 = Analysis(path_to_poscar="TestData/BaTiO3/POSCAR",
                                       path_to_cohpcar="TestData/BaTiO3/COHPCAR.lobster",
                                       path_to_icohplist="TestData/BaTiO3/ICOHPLIST.lobster",
                                       path_to_charge="TestData/BaTiO3/CHARGE.lobster", whichbonds="cation-anion", \
                                       cutoff_icohp=0.1)

        self.describe_BaTiO3 = Description(self.analyse_BaTiO3)

        self.analyse_BaTaO2N1 = Analysis(path_to_poscar="TestData/BaTaO2N1/POSCAR.gz",
                                         path_to_cohpcar="TestData/BaTaO2N1/COHPCAR.lobster.gz",
                                         path_to_icohplist="TestData/BaTaO2N1/ICOHPLIST.lobster.gz",
                                         path_to_charge="TestData/BaTaO2N1/CHARGE.lobster.gz",
                                         whichbonds="cation-anion", \
                                         cutoff_icohp=0.1)
        self.describe_BaTaO2N1 = Description(self.analyse_BaTaO2N1)

        self.describe_BaTiO3 = Description(self.analyse_BaTiO3)

        self.analyse_CdF = Analysis(path_to_poscar="TestData/CdF/POSCAR",
                                    path_to_cohpcar="TestData/CdF/COHPCAR.lobster",
                                    path_to_icohplist="TestData/CdF/ICOHPLIST.lobster",
                                    path_to_charge="TestData/CdF/CHARGE.lobster",
                                    whichbonds="cation-anion", \
                                    cutoff_icohp=0.1)
        self.describe_CdF = Description(self.analyse_CdF)

        self.analyse_NaCl_distorted = Analysis(path_to_poscar="TestData/NaCl_distorted/POSCAR",
                                               path_to_cohpcar="TestData/NaCl_distorted/COHPCAR.lobster",
                                               path_to_icohplist="TestData/NaCl_distorted/ICOHPLIST.lobster",
                                               path_to_charge="TestData/NaCl_distorted/CHARGE.lobster",
                                               whichbonds="cation-anion", \
                                               cutoff_icohp=0.1)

        self.describe_NaCl_distorted = Description(self.analyse_NaCl_distorted)

        self.analyse_NaCl_spin = Analysis(path_to_poscar="TestData/NaCl_spin/POSCAR",
                                          path_to_cohpcar="TestData/NaCl_spin/COHPCAR.lobster",
                                          path_to_icohplist="TestData/NaCl_spin/ICOHPLIST.lobster",
                                          path_to_charge="TestData/NaCl_spin/CHARGE.lobster",
                                          whichbonds="cation-anion", \
                                          cutoff_icohp=0.1, summed_spins=False)
        self.describe_NaCl_spin = Description(self.analyse_NaCl_spin)

    def test_coordination_environment_to_text(self):
        results_dict = {
            "S:1": "single (CN=1)",
            "L:2": "linear (CN=2)",
            "A:2": "angular (CN=2)",
            "TL:3": "trigonal planar (CN=3)",
            "TY:3": "triangular non-coplanar (CN=3)",
            "TS:3": "t-shaped (CN=3)",
            "T:4": "tetrahedral (CN=4)",
            "S:4": "square planar (CN=4)",
            "SY:4": "square non-coplanar (CN=4)",
            "SS:4": "see-saw like (CN=4)",
            "PP:5": "pentagonal (CN=5)",
            "S:5": "square pyramidal (CN=5)",
            "T:5": "trigonal bipyramidal (CN=5)",
            "O:6": "octahedral (CN=6)",
            "T:6": "trigonal prismatic (CN=6)",
            "PP:6": "pentagonal pyramidal (CN=6)",
            "PB:7": "pentagonal bipyramidal (CN=7)",
            "ST:7": "square-face capped trigonal prismatic (CN=7)",
            "ET:7": "end-trigonal-face capped trigonal prismatic (CN=7)",
            "FO:7": "face-capped octahedron (CN=7)",
            "C:8": "cubic (CN=8)",
            "SA:8": "sqaure antiprismatic (CN=8)",
            "SBT:8": "square-face bicapped trigonal prismatic (CN=8)",
            "TBT:8": "triangular-face bicapped trigonal prismatic (CN=8)",
            "DD:8": "dodecahedronal (with triangular faces) (CN=8)",
            "DDPN:8": "dodecahedronal (with triangular faces - p2345 plane normalized) (CN=8)",
            "HB:8": "hexagonal bipyramidal (CN=8)",
            "BO_1:8": "bicapped octahedral (opposed cap faces) (CN=8)",
            "BO_2:8": "bicapped octahedral (cap faces with one atom in common) (CN=8)",
            "BO_3:8": "bicapped octahedral (cap faces with one edge in common) (CN=8)",
            "TC:9": "triangular cupola (CN=9)",
            "TT_1:9": "Tricapped triangular prismatic (three square - face caps) (CN=9)",
            "TT_2:9": "Tricapped triangular prismatic (two square - face caps and one triangular - face cap) (CN=9)",
            "TT_3:9": "Tricapped triangular prism (one square - face cap and two triangular - face caps) (CN=9)",
            "HD:9": "Heptagonal dipyramidal (CN=9)",
            "TI:9": "tridiminished icosohedral (CN=9)",
            "SMA:9": "Square-face monocapped antiprism (CN=9)",
            "SS:9": "Square-face capped square prismatic (CN=9)",
            "TO_1:9": "Tricapped octahedral (all 3 cap faces share one atom) (CN=9)",
            "TO_2:9": "Tricapped octahedral (cap faces are aligned) (CN=9)",
            "TO_3:9": "Tricapped octahedron (all 3 cap faces are sharing one edge of a face) (CN=9)",
            "PP:10": "Pentagonal prismatic (CN=10)",
            "PA:10": "Pentagonal antiprismatic (CN=10)",
            "SBSA:10": "Square-face bicapped square antiprismatic (CN=10)",
            "MI:10": "Metabidiminished icosahedral (CN=10)",
            "S:10": "sphenocoronal (CN=10)",
            "H:10": "Hexadecahedral (CN=10)",
            "BS_1:10": "Bicapped square prismatic (opposite faces) (CN=10)",
            "BS_1:10": "Bicapped square prismatic (opposite faces) (CN=10)",
            "BS_2:10": "Bicapped square prism(adjacent faces) (CN=10)",
            "TBSA:10": "Trigonal-face bicapped square antiprismatic (CN=10)",
            "PCPA:11": "Pentagonal - face capped pentagonal antiprismatic (CN=11)",
            "H:11": "Hendecahedral (CN=11)",
            "SH:11": "Sphenoid hendecahedral (CN=11)",
            "CO:11": "Cs - octahedral (CN=11)",
            "DI:11": "Diminished icosahedral (CN=12)",
            "I:12": "Icosahedral (CN=12)",
            "PBP: 12": "Pentagonal - face bicapped pentagonal prismatic (CN=12)",
            "TT:12": "Truncated tetrahedral (CN=12)",
            "C:12": "Cuboctahedral (CN=12)",
            "AC:12": "Anticuboctahedral (CN=12)",
            "SC:12": "Square cupola (CN=12)",
            "S:12": "Sphenomegacorona (CN=12)",
            "HP:12": "Hexagonal prismatic (CN=12)",
            "HA:12": "Hexagonal antiprismatic (CN=12)",
            "SH:13": "Square-face capped hexagonal prismatic (CN=13)",
            "H:5": "H:5"
        }
        for key, items in results_dict.items():
            self.assertEqual(Description._coordination_environment_to_text(key), items)

    def test_plot(self):
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            self.describe_NaCl.plot_cohps(save=True, filename=tmp.name, xlim=[-4, 4])
            self.assertTrue(os.path.exists(tmp.name))
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            self.describe_NaCl_spin.plot_cohps(save=True, filename=tmp.name, xlim=[-4, 4])
            self.assertTrue(os.path.exists(tmp.name))

    def test_write_descritoin(self):
        self.describe_NaCl.write_description()

    def test_text(self):
        self.assertEqual(self.describe_CdF.text, [
            'The compound CdF2 has 1 symmetry-independent cation(s) with relevant cation-anion interactions: Cd1.',
            'Cd1 has a cubic (CN=8) coordination environment. It has 8 Cd-F (mean ICOHP: -0.62 eV, antibonding  interaction below EFermi) bonds.'])
        self.assertEqual(self.describe_NaCl.text, [
            'The compound NaCl has 1 symmetry-independent cation(s) with relevant cation-anion interactions: Na1.',
            'Na1 has an octahedral (CN=6) coordination environment. It has 6 Na-Cl (mean ICOHP: -0.57 eV, antibonding  interaction below EFermi) bonds.'])
        self.assertEqual(self.describe_NaCl.text, [
            'The compound NaCl has 1 symmetry-independent cation(s) with relevant cation-anion interactions: Na1.',
            'Na1 has an octahedral (CN=6) coordination environment. It has 6 Na-Cl (mean ICOHP: -0.57 eV, antibonding  interaction below EFermi) bonds.'])


if __name__ == '__main__':
    unittest.main()
