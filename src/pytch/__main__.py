#!/usr/bin/python3
"""
Pytch - Pytch Yields Technical Characteristics Hastily
Copyright (c) 2023, Krit Dass

This file is part of Pytch.

Pytch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

Pytch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License 
along with Pytch. If not, see <https://www.gnu.org/licenses/>.
"""

from os import getlogin, mkdir
from os.path import isdir, isfile, expanduser
from copy import deepcopy
from toml import load, dump
from argparse import Action, ArgumentParser, RawTextHelpFormatter
from pytch.funcs import (
    get_output,
    get_name,
    get_uptime,
    get_shell,
    get_packages,
    get_memory,
    get_kernel,
    ascii_image,
    ascii_text,
    color,
)

default_config = {
    "attributes": {
        "user": {"name": "user", "value": getlogin(), "icon": "", "color": "red"},
        "os": {
            "name": "os",
            "value": (
                get_name()
                if get_name() != "Darwin"
                else get_output("sw_vers -productName").strip()
            ),
            "icon": "",
            "color": "yellow",
        },
        "kernel": {
            "name": "kernel",
            "value": get_kernel(),
            "icon": "",
            "color": "green",
        },
        "uptime": {
            "name": "uptime",
            "value": get_uptime(),
            "icon": "",
            "color": "blue",
        },
        "shell": {
            "name": "shell",
            "value": get_shell(),
            "icon": "",
            "color": "magenta",
        },
        "packages": {
            "name": "pkgs",
            "value": get_packages(),
            "icon": "",
            "color": "red",
        },
        "memory": {
            "name": "memory",
            "value": get_memory(),
            "icon": "󰍛",
            "color": "cyan",
        },
    },
    "attributes_list": [
        "user",
        "os",
        "kernel",
        "uptime",
        "shell",
        "packages",
        "memory",
    ],
    "show_icons": True,
    "logo": {
        "name": "auto",
        "type": "ascii_image",
        "ascii_text_font": "small",
        "ascii_text_color": "cyan",
        "ascii_image_color": "auto",
    },
}


class GenerateDefaultConfig(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        proceed = True
        config = deepcopy(default_config)
        for key in config["attributes"].keys():
            config["attributes"][key]["value"] = "auto"

        if isfile(expanduser("~/.config/pytch/config.toml")):
            overwrite = input(
                f"A configuration file for Pytch already exists at {expanduser('~/.config/pytch/config.toml')}. Would you like to overwrite this file? [y/N] "
            )
            if overwrite.lower() not in ["y", "yes"]:
                proceed = False
        elif not isdir(expanduser("~/.config/pytch")):
            mkdir(expanduser("~/.config/pytch"))

        if proceed:
            with open(expanduser("~/.config/pytch/config.toml"), "w") as config_file:
                dump(config, config_file)
            print("Successfully written.")
        else:
            print("Exiting without writing.")

        setattr(namespace, self.dest, values)
        parser.exit()


def merge(src, dest):
    dest_copy = deepcopy(dest)
    for key, val in src.items():
        dest_key_val = dest_copy.get(key)
        if isinstance(val, dict) and isinstance(dest_key_val, dict):
            dest_copy[key] = merge(val, dest_copy.setdefault(key, {}))
        elif val != "auto":
            dest_copy[key] = val
    return dest_copy


def load_config(config_file):
    config = {}
    config_file = config_file or expanduser("~/.config/pytch/config.toml")
    if isfile(config_file):
        config = load(config_file)

    return merge(config, default_config)


def main():
    parser = ArgumentParser(
        prog="pytch",
        description="Pytch Yields Technical Characteristics Hastily",
        epilog="""Pytch Copyright (c) 2023 Krit Dass
This program is licensed under the GNU General Public License (see https://www.gnu.org/licenses/).
Report bugs to https://github.com/kritdass/pytch/issues.""",
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument(
        "-l",
        "--logo",
        metavar="DISTRO",
        dest="logo",
        help="use an alternate distribution's logo",
    )

    parser.add_argument("-v", "--version", action="version", version="2.0.0")

    parser.add_argument(
        "-g",
        "--gen-default-config",
        nargs=0,
        action=GenerateDefaultConfig,
        help="generates the default config",
    )

    parser.add_argument(
        "-c",
        "--config",
        metavar="CONFIG_FILE",
        dest="config",
        help=f"use a config file other than the one located at {expanduser('~/.config/pytch/config.toml')}",
    )

    args = parser.parse_args()

    config = load_config(args.config)
    attrs = [config["attributes"][attr] for attr in config["attributes_list"]]
    show_icons = config["show_icons"]
    logo = args.logo or (
        config["logo"]["name"] if config["logo"]["name"] != "auto" else get_name()
    )
    logo_art = (
        ascii_text(logo, config["logo"]["ascii_text_color"], font=config["logo"]["ascii_text_font"])
        if config["logo"]["type"] == "ascii_text"
        else ascii_image(logo, config["logo"]["ascii_image_color"])
    )
    print("\n" + logo_art["art"])

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
    gap = logo_art["length"] - name_width - value_width - 8

    print(
        "╭"
        + ("─" * (5 if show_icons else 2))
        + "╮"
        + (" " * (name_width + value_width + gap - 2))
        + "╭─╮"
    )

    for attr in attrs:
        if attr["name"] == "pkgs":
            if len(attr["value"]) > 1:
                for i, packager in enumerate(attr["value"]):
                    print(
                        "│ "
                        + color(
                            (
                                " "
                                + (attr["icon"] if not (i and show_icons) else " ")
                                + "  "
                            )
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
                ((" " + attr["icon"] + " " if show_icons else "") + " ")
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

    print(
        "╰"
        + ("─" * (5 if show_icons else 2))
        + "╯"
        + (" " * (name_width + value_width + gap - 2))
        + "╰─╯"
        + "\n"
    )
