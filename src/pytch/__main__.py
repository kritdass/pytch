#!/usr/bin/env python3

from os import getlogin
from argparse import ArgumentParser
from pytch.funcs import (
    get_output,
    get_name,
    get_uptime,
    get_shell,
    get_packages,
    get_memory,
    get_kernel,
    art,
    color,
)


def main():
    parser = ArgumentParser(
        prog="pytch",
        description="Pytch Yields Technical Characteristics Hastily",
        epilog="Report bugs to https://github.com/kritdass/pytch/issues",
    )

    parser.add_argument(
        "-l",
        "--logo",
        metavar="DISTRO",
        dest="logo",
        help="use an alternate distribution's logo",
    )

    parser.add_argument("-v", "--version", action="version", version="1.2.0")

    args = parser.parse_args()

    attrs = [
        {"name": "user", "value": getlogin(), "icon": "", "color": "red"},
        {
            "name": "os",
            "value": (
                get_name()
                if get_name() != "Darwin"
                else get_output("sw_vers -productName").strip()
            ),
            "icon": "",
            "color": "yellow",
        },
        {"name": "kernel", "value": get_kernel(), "icon": "", "color": "green"},
        {"name": "uptime", "value": get_uptime(), "icon": "", "color": "blue"},
        {"name": "shell", "value": get_shell(), "icon": "", "color": "magenta"},
        {"name": "pkgs", "value": get_packages(), "icon": "", "color": "red"},
        {"name": "memory", "value": get_memory(), "icon": "󰍛", "color": "cyan"},
    ]

    print("\n" + art(args.logo or get_name())["art"])

    name_width = max([len(attr["name"]) for attr in attrs])
    value_width = max(
        [
            (
                len(attr["value"])
                if isinstance(attr["value"], str)
                else max([len(s) for s in attr["value"]])
            )
            for attr in attrs
        ]
    )
    gap = art(args.logo or get_name())["length"] - name_width - value_width - 8

    print("╭─────╮" + (" " * (name_width + value_width + gap - 2)) + "╭─╮")

    for attr in attrs:
        if attr["name"] == "pkgs":
            if len(attr["value"]) > 1:
                for i, packager in enumerate(attr["value"]):
                    print(
                        "│ "
                        + color(
                            (" " + (attr["icon"] if not i else " ") + "  ")
                            + (attr["name"] if not i else "")
                            + (name_width + gap - (len(attr["name"]) if not i else 0))
                            * " ",
                            attr["color"],
                        )
                        + color(
                            (" " * (value_width - len(packager))) + packager,
                            attr["color"],
                        )
                        + " │"
                    )
                continue
            else:
                attr["value"] = attr["value"][0].split(" ")[0]

        print(
            "│ "
            + color(
                (" " + attr["icon"] + "  ")
                + attr["name"]
                + (name_width + gap - len(attr["name"])) * " ",
                attr["color"],
            )
            + color(
                (" " * (value_width - len(attr["value"]))) + attr["value"],
                attr["color"],
            )
            + " │"
        )

    print("╰─────╯" + (" " * (name_width + value_width + gap - 2)) + "╰─╯" + "\n")
