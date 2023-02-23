# Copyright (c) lobsterpy development team
# Distributed under the terms of a BSD 3-Clause "New" or "Revised" License

"""
Script to analyze Lobster outputs from the command line
"""
from __future__ import annotations

import argparse
import json
from math import log, sqrt
from pathlib import Path

import matplotlib.style
from pymatgen.electronic_structure.cohp import CompleteCohp

from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description
from lobsterpy.plotting import PlainCohpPlotter, get_style_list


def main() -> None:
    """Entry point for setup.py installer"""
    args = get_parser().parse_args()
    run(args)


def get_parser() -> argparse.ArgumentParser:
    """Construct argumentparser with subcommands and sections"""
    parser = argparse.ArgumentParser(description="Analyze and plot results from Lobster runs.")

    # Arguments common to all actions
    input_parent = argparse.ArgumentParser(add_help=False)
    input_file_group = input_parent.add_argument_group("Input files")
    input_file_group.add_argument(
        "--poscar",
        "--POSCAR",
        dest="poscar",
        default="POSCAR",
        type=Path,
        help='path to POSCAR. Default is "POSCAR"',
    )
    input_file_group.add_argument(
        "--charge",
        default="CHARGE.lobster",
        type=Path,
        help='path to Charge.lobster. Default is "CHARGE.lobster"',
    )
    input_file_group.add_argument(
        "--icohplist",
        default="ICOHPLIST.lobster",
        type=Path,
        help='path to ICOHPLIST.lobster. Default is "ICOHPLIST.lobster"',
    )
    input_file_group.add_argument(
        "--cohpcar",
        default="COHPCAR.lobster",
        type=Path,
        help=(
            'path to COHPCAR.lobster. Default is "COHPCAR.lobster". This argument '
            "will also be read when COBICARs or COOPCARs are plotted."
        ),
    )
    input_file_group.add_argument(
        "--incar",
        default="INCAR",
        type=Path,
        help=('path to INCAR. Default is "INCAR".'),
    )
    input_file_group.add_argument(
        "--potcar",
        default="POTCAR",
        type=Path,
        help=('path to POTCAR. Default is "POTCAR".'),
    )

    output_parent = argparse.ArgumentParser(add_help=False)
    output_file_group = output_parent.add_argument_group("Output files")
    output_file_group.add_argument(
        "--incar-out",
        "--incarout",
        dest="incarout",
        default="INCAR.lobsterpy",
        type=Path,
        help='path to INCAR that will be generated by lobsterpy. Default is "INCAR.lobsterpy"',
    )
    output_file_group.add_argument(
        "--lobsterin-out",
        "--lobsterinout",
        dest="lobsterinout",
        default="lobsterin.lobsterpy",
        type=Path,
        help='base for path to lobsterins that will be generated by lobsterpy. Default is "lobsterin.lobsterpy"',
    )
    output_file_group.add_argument(
        "--overwrite",
        "--overwrite-files",
        dest="overwrite",
        default=False,
        action="store_true",
        help="overwrites already created INCARs an lobsterins with the give name.",
    )
    # TODO: Add some output arguments: options to supply your own basis
    output_file_group.add_argument(
        "--userbasis",
        "--user-basis",
        default=None,
        type=_element_basis,
        nargs="+",
        help="This setting will rely on a specific basis provided by the user "
        "(e.g.,  --userbasis Cr.3d.3p.4s N.2s.2p). Default is None.",
    )

    plotting_parent = argparse.ArgumentParser(add_help=False)
    plotting_group = plotting_parent.add_argument_group("Plotting")

    broadening_group = plotting_group.add_mutually_exclusive_group()
    broadening_group.add_argument_group("Broadening")
    broadening_group.add_argument(
        "--sigma",
        type=float,
        default=None,
        help="Standard deviation of Gaussian broadening.",
    )

    broadening_group.add_argument(
        "--fwhm",
        type=float,
        default=None,
        help="Full-width-half-maximum of Gaussian broadening.",
    )

    plotting_group.add_argument(
        "--integrated",
        action="store_true",
        help="Show integrated cohp/cobi/coop plots.",
    )

    plotting_group.add_argument(
        "--ylim",
        dest="ylim",
        nargs=2,
        default=None,
        type=float,
        help="Energy range for plots",
    )
    plotting_group.add_argument(
        "--xlim",
        dest="xlim",
        nargs=2,
        default=None,
        type=float,
        help="COHP/COBI/COOP range for plots",
    )

    plotting_group.add_argument(
        "--style",
        type=str,
        nargs="+",
        default=None,
        help="Matplotlib style sheet(s) for plot appearance",
    )
    plotting_group.add_argument(
        "--no-base-style",
        "--nobasestyle",
        action="store_true",
        dest="no_base_style",
        help=(
            "Disable inbuilt style entirely. This may prevent interference with external "
            "stylesheets when using --style."
        ),
    )
    plotting_group.add_argument("--title", type=str, default="", help="Plot title")
    plotting_group.add_argument(
        "--save-plot",
        "--saveplot",
        "-s",
        type=Path,
        metavar="FILENAME",
        default=None,
        dest="save_plot",
        help="Save plot to file",
    )
    plotting_group.add_argument("--width", type=float, default=None, help="Plot width in inches")
    plotting_group.add_argument("--height", type=float, default=None, help="Plot height in inches")
    plotting_group.add_argument("--fontsize", "--font-size", type=float, default=None, help="Base font size")

    auto_parent = argparse.ArgumentParser(add_help=False)
    auto_group = auto_parent.add_argument_group("Automatic analysis")
    auto_group.add_argument(
        "--json",
        nargs="?",
        type=Path,
        default=None,
        metavar="FILENAME",
        const=Path("lobsterpy.json"),
        help="Write a JSON file with the most important information",
    )
    auto_group.add_argument(
        "--allbonds",
        "--all-bonds",
        action="store_true",
        default=False,
        help="This option will force the automatc analysis to consider"
        " all bonds, not only cation-anion bonds (default) ",
    )

    subparsers = parser.add_subparsers(
        dest="action",
        required=True,
        help="Use -h/--help after the chosen subcommand to see further options.",
    )
    subparsers.add_parser(
        "description",
        parents=[input_parent, auto_parent],
        help=(
            "Deliver a text description of the COHP results from Lobster "
            "and VASP. Implementation of COBIs and COOPs will follow."
        ),
    )

    subparsers.add_parser(
        "automatic-plot",
        aliases=["automaticplot"],
        parents=[input_parent, auto_parent, plotting_parent],
        help=(
            "Plot most important COHPs automatically. Implementation "
            "of COBIs and COOPs will follow. This option also includes an automatic description."
        ),
    )

    subparsers.add_parser(
        "create-inputs",
        aliases=["createinputs"],
        parents=[input_parent, output_parent],
        help=("Will create inputs for lobster computation. It only works with PBE POTCARs."),
    )

    # Mode for normal plotting (without automatic detection of relevant COHPs)
    plot_parser = subparsers.add_parser(
        "plot",
        parents=[input_parent, plotting_parent],
        help="Plot specific COHPs/COBIs/COOPs based on bond numbers.",
    )

    plot_parser.add_argument(
        "bond_numbers",
        nargs="+",
        type=int,
        help="List of bond numbers, determining COHPs/COBIs/COOPs to include in plot.",
    )
    plot_coops_cobis = plot_parser.add_mutually_exclusive_group()
    plot_coops_cobis.add_argument(
        "--cobis",
        "--cobi",
        action="store_true",
        help="Plot COBIs",
    )
    plot_coops_cobis.add_argument(
        "--coops",
        "--coop",
        action="store_true",
        help="Plot COOPs",
    )
    plot_grouping = plot_parser.add_mutually_exclusive_group()
    plot_grouping.add_argument(
        "--summed",
        action="store_true",
        help="Show a summed COHP",
    )
    plot_grouping.add_argument(
        "--orbitalwise",
        dest="orbitalwise",
        nargs="+",
        default=None,
        type=str,
        help=(
            "Plot cohps of specific orbitals. e.g. to plot 2s-2s interaction of "
            'bond with label 1, use "lobsterpy plot 1 --orbitalwise 2s-2s". '
            'To plot all orbitalwise cohps of one bond, you can use "all" instead of "2s-2s". '
            "To plot orbitalwise interactions of more than one bond, use, for example, "
            '"lobsterpy plot 1 1 --orbitalwise "3s-3s" "2px-3s"'
        ),
    )
    return parser


def _element_basis(string: str):
    """
    Parse element and basis from string
    Args: str
    Returns: element, basis
    """
    cut_list = string.split(".")
    element = cut_list[0]
    basis = " ".join(cut_list[1:])
    return element, basis


def _user_figsize(width, height, aspect=None):
    """Get figsize options from user input, if any

    If only width x or height is provided, use a target aspect ratio to derive
    the other one.

    Returns a dict which can be merged into style kwargs
    """
    if width is None and height is None:
        return {}
    if width is not None and height is not None:
        return {"figure.figsize": (width, height)}

    if aspect is None:
        aspect = (sqrt(5) + 1) / 2  # Golden ratio
    if width is None:
        return {"figure.figsize": (height * aspect, height)}
    return {"figure.figsize": (width, width / aspect)}


# TODO: add automatic functionality for COBIs, COOPs
def run(args):
    """

    Args:
        args: args for cli

    """
    if args.action == "automaticplot":
        args.action = "automatic-plot"

    if args.action in ["description", "automatic-plot"]:
        if args.allbonds:
            whichbonds = "all"
        else:
            whichbonds = "cation-anion"
        analyse = Analysis(
            path_to_poscar=args.poscar,
            path_to_charge=args.charge,
            path_to_cohpcar=args.cohpcar,
            path_to_icohplist=args.icohplist,
            whichbonds=whichbonds,
        )

        describe = Description(analysis_object=analyse)
        describe.write_description()

        if args.json is not None:
            analysedict = analyse.condensed_bonding_analysis
            with open(args.json, "w") as fd:
                json.dump(analysedict, fd)

    if args.action in ["plot", "automatic-plot"]:
        style_kwargs = {}
        style_kwargs.update(_user_figsize(args.width, args.height))
        if args.fontsize:
            style_kwargs.update({"font.size": args.fontsize})

        style_list = get_style_list(no_base_style=args.no_base_style, styles=args.style, **style_kwargs)
        matplotlib.style.use(style_list)

        if args.sigma:
            sigma = args.sigma
        elif args.fwhm:
            sigma = args.fwhm / (2 * sqrt(2 * log(2)))
        else:
            sigma = None

    if args.action in ["automatic-plot"]:
        describe.plot_cohps(
            ylim=args.ylim,
            xlim=args.xlim,
            integrated=args.integrated,
            save=args.save_plot is not None,
            filename=args.save_plot,
            title=args.title,
            sigma=sigma,
        )

    if args.action == "plot":
        if args.cobis:
            filename = args.cohpcar.parent / "COBICAR.lobster"
            options = {"are_cobis": True, "are_coops": False}
        elif args.coops:
            filename = args.cohpcar.parent / "COOPCAR.lobster"
            options = {"are_cobis": False, "are_coops": True}
        else:
            filename = args.cohpcar
            options = {"are_cobis": False, "are_coops": False}

        completecohp = CompleteCohp.from_file(fmt="LOBSTER", filename=filename, structure_file=args.poscar, **options)
        cp = PlainCohpPlotter(**options)

        if not args.summed:
            # TODO: add checks for label in allewod labels -> print all labels
            # TODO: add check if args.oribtalwise is exactly as long as labels
            # TODO: add check if orbital is in args.orbitalwise

            for label in args.bond_numbers:
                if str(label) not in completecohp.bonds.keys():
                    raise IndexError(
                        "The provided bond label " + str(label) + " is not available in ICO**LIST.lobster.\n "
                        "Allowed options are in this list: \n"
                        + str([int(listi) for listi in list(completecohp.bonds.keys())])
                    )

            if not args.orbitalwise:
                for label in args.bond_numbers:
                    cp.add_cohp(label, completecohp.get_cohp_by_label(label=str(label)))
            else:
                if len(args.bond_numbers) != len(args.orbitalwise):
                    raise IndexError(
                        "Please provide as mainy orbitals as bond labels,"
                        " e.g., lobsterpy plot 1 1 --orbitalwise '2s-2s' '2s-2px'"
                    )

                for ilabel, label in enumerate(args.bond_numbers):
                    orbitals = args.orbitalwise[ilabel]

                    availableorbitals = list(completecohp.orb_res_cohp[str(label)].keys())
                    orbitaloptions = [*availableorbitals, "all"]

                    if orbitals not in orbitaloptions:
                        raise IndexError(
                            "Orbital in not available for current bond. \n"
                            "For bond "
                            + str(label)
                            + " only the following orbital options are available: \n"
                            + str(orbitaloptions)
                        )

                    if orbitals != "all":
                        cp.add_cohp(
                            str(label) + ": " + orbitals,
                            completecohp.get_orbital_resolved_cohp(label=str(label), orbitals=orbitals),
                        )
                    else:
                        for orbitals in availableorbitals:
                            cp.add_cohp(
                                str(label) + ": " + orbitals,
                                completecohp.get_orbital_resolved_cohp(label=str(label), orbitals=orbitals),
                            )
        else:
            cp.add_cohp(
                str(args.bond_numbers),
                completecohp.get_summed_cohp_by_label_list(label_list=[str(label) for label in args.bond_numbers]),
            )

        plt = cp.get_plot(integrated=args.integrated, xlim=args.xlim, ylim=args.ylim, sigma=sigma)

        ax = plt.gca()
        ax.set_title(args.title)

        if args.save_plot is None:
            plt.show()
        else:
            fig = plt.gcf()
            fig.savefig(args.save_plot)
    if args.action == "create-inputs":
        from pymatgen.core.structure import Structure
        from pymatgen.io.lobster import Lobsterin

        if args.userbasis is None:
            # This will rely on standard basis files as stored in pymatgen

            potcar_names = Lobsterin._get_potcar_symbols(POTCAR_input=args.potcar)

            list_basis_dict = Lobsterin.get_all_possible_basis_functions(
                structure=Structure.from_file(args.poscar), potcar_symbols=potcar_names
            )

            for ibasis, basis_dict in enumerate(list_basis_dict):
                lobsterinput = Lobsterin.standard_calculations_from_vasp_files(
                    args.poscar,
                    args.incar,
                    None,
                    option="standard",
                    dict_for_basis=basis_dict,
                )

                lobsterin_path = Path(str(args.lobsterinout) + "-" + str(ibasis))
                incar_path = Path(str(args.incarout) + "-" + str(ibasis))

                if (not lobsterin_path.is_file() and not incar_path.is_file()) or (args.overwrite):
                    lobsterinput.write_lobsterin(lobsterin_path)
                    lobsterinput.write_INCAR(
                        incar_input=args.incar,
                        incar_output=incar_path,
                        poscar_input=args.poscar,
                        isym=0,
                    )
                else:
                    raise ValueError('please use "--overwrite" if you would like to overwrite existing lobster inputs')
        else:
            # convert list userbasis to dict
            userbasis = {}
            for userbasis_single in args.userbasis:
                userbasis[userbasis_single[0]] = userbasis_single[1]

            lobsterinput = Lobsterin.standard_calculations_from_vasp_files(
                args.poscar,
                args.incar,
                None,
                option="standard",
                dict_for_basis=userbasis,
            )

            lobsterin_path = Path(str(args.lobsterinout) + "-" + str(0))
            incar_path = Path(str(args.incarout) + "-" + str(0))

            if (not lobsterin_path.is_file() and not incar_path.is_file()) or (args.overwrite):
                lobsterinput.write_lobsterin(lobsterin_path)
                lobsterinput.write_INCAR(
                    incar_input=args.incar,
                    incar_output=incar_path,
                    poscar_input=args.poscar,
                    isym=0,
                )
            else:
                raise ValueError('please use "--overwrite" if you would like to overwrite existing lobster inputs')


if __name__ == "__main__":
    main()
