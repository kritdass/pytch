#!/usr/bin/env python3

from os import getlogin
from argparse import ArgumentParser
from pytch.funcs import (
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

    parser.add_argument("-v", "--version", action="version", version="1.0.1")

    args = parser.parse_args()

    attrs = [
        {"name": "user", "value": getlogin(), "icon": "", "color": "red"},
        {"name": "os", "value": get_name(), "icon": "", "color": "yellow"},
        {"name": "kernel", "value": get_kernel(), "icon": "", "color": "green"},
        {"name": "uptime", "value": get_uptime(), "icon": "", "color": "blue"},
        {"name": "shell", "value": get_shell(), "icon": "", "color": "magenta"},
        {"name": "pkgs", "value": get_packages(), "icon": "", "color": "red"},
        {"name": "memory", "value": get_memory(), "icon": "󰍛", "color": "cyan"},
    ]

    print("\n" + art(args.logo or get_name())["art"])

    name_width = max([len(attr["name"]) for attr in attrs])
    value_width = max([len(attr["value"]) for attr in attrs])
    gap = art(args.logo or get_name())["length"] - name_width - value_width - 8

    print("╭─────╮" + (" " * (name_width + value_width + gap - 2)) + "╭─╮")

    for attr in attrs:
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
