#!/usr/bin/env python3

import os
import subprocess
import distro
import platform
import psutil
from termcolor import colored
from art import text2art


def get_uptime():
    with open("/proc/uptime", "r") as f:
        seconds = int(float(f.readline().split()[0]))
        seconds -= (hours := seconds // 3600) * 3600
        minutes = seconds // 60
    return f"{hours}h {minutes}m"


def get_shell():
    shell_path = os.environ["SHELL"]
    return shell_path.split("/")[-1]


def get_memory():
    percent_mem = psutil.virtual_memory().percent
    return f"{percent_mem}%"


def get_packages():
    def get_lines(cmd):
        packages = subprocess.check_output([cmd], shell=True, text=True)
        num_pkgs = len(packages.split("\n")) - 1
        return str(num_pkgs)

    match distro.id():
        case "ubuntu" | "debian" | "linuxmint" | "pop" | "raspbian":
            return get_lines("dpkg -l")
        case "arch" | "endeavouros" | "artix" | "manjaro" | "arcolinux" | "archraft" | "garuda":
            return get_lines("pacman -Qq")
        case "nixos":
            return get_lines("nix-store -qR /run/current-system/sw ~/.nix-profile")
        case "fedora" | "centos" | "sles" | "opensuse" | "mandriva" | "scientific" | "rhel":
            return get_lines("rpm -qa")
        case "void":
            return get_lines("xbps-query -l")
        case "gentoo" | "chromeos":
            return get_lines("ls -d /var/db/pkg/*/*| cut -f5- -d/")
        case _:
            return "0/0"


attrs = [
    {"name": "user", "value": os.getlogin(), "icon": "", "color": "red"},
    {"name": "os", "value": distro.name(), "icon": "", "color": "yellow"},
    {"name": "kernel", "value": platform.release(), "icon": "", "color": "green"},
    {"name": "uptime", "value": get_uptime(), "icon": "", "color": "blue"},
    {"name": "shell", "value": get_shell(), "icon": "", "color": "magenta"},
    {"name": "pkgs", "value": get_packages(), "icon": "", "color": "light_red"},
    {"name": "memory", "value": get_memory(), "icon": "󰍛", "color": "cyan"},
]

print(colored(text2art(distro.name()), "cyan"), end="")

gap = 5
width = max([len(attr["name"]) for attr in attrs]) + gap

for index, attr in enumerate(attrs):
    print(
        colored(
            " "
            + attr["icon"]
            + "  "
            + attr["name"]
            + (width - len(attr["name"])) * " "
            + attr["value"],
            attr["color"],
        )
    )

print()
