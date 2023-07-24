from os import walk, environ
from os.path import isfile
from platform import release
from subprocess import check_output, DEVNULL, CalledProcessError
from re import search, findall, sub, split
from pytch.art import art_dict


def color(text, color):
    colors = {
        "black": 90,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
    }
    return f"\033[{colors[color]}m{text}\033[0m"


def art(distro):
    length = max(
        [
            len(sub(r"\$\{c[1-6]\}", "", line))
            for line in art_dict[distro]["ascii"].split("\n")
        ]
    )

    segments = split(r"\$\{c[1-6]\}", art_dict[distro]["ascii"])[1:]
    colors = [
        int(pattern[3]) - 1
        for pattern in findall(r"\$\{c[1-6]\}", art_dict[distro]["ascii"])
    ]

    result = ""
    for i in range(len(segments)):
        result += color(segments[i], art_dict[distro]["colors"][colors[i]])

    min_length = 45
    if length < min_length:
        spacer = " " * ((min_length - length) // 2)
        result = "\n".join([spacer + line + spacer for line in result.split("\n")])
        length = min_length

    return {"art": result, "length": length}


def get_name():
    def get_lsb_release():
        try:
            return check_output(["lsb_release", "-a"], stderr=DEVNULL, text=True)
        except (OSError, CalledProcessError):
            return ""

    def get_distro_release():
        for _, _, files in walk("/etc"):
            for release_file in files:
                if search("(-|_)(release|version)", release_file):
                    with open(release_file, "r") as file:
                        for pair in file.read().split("\n"):
                            if pair.split("=")[0] == "DISTRIB_ID":
                                return pair.split("=")[1]
        return ""

    name = ""
    if isfile("/etc/os-release") or isfile("/usr/lib/os-release"):
        release_file = (
            "/etc/os-release" if isfile("/etc/os-release") else "/usr/lib/os-release"
        )
        with open(release_file, "r") as os_release:
            os_release = os_release.read().split("\n")
            for pair in os_release:
                if pair.split("=")[0] == "NAME":
                    name = pair.split("=")[1]
    elif get_lsb_release():
        lsb_release = get_lsb_release().split("\n")
        for pair in lsb_release:
            if pair.split(":")[0] == "Distributor ID":
                name = pair.split(":")[1].strip()
    elif get_distro_release():
        name = get_distro_release()

    return "RHEL" if name.startswith("Red Hat") else name.replace('"', "")


def get_kernel():
    return release().split("-")[0]


def get_uptime():
    with open("/proc/uptime", "r") as file:
        seconds = int(float(file.readline().split()[0]))
        hours = seconds // 3600
        seconds -= hours * 3600
        minutes = seconds // 60
    return f"{hours}h {minutes}m"


def get_shell():
    shell_path = environ["SHELL"]
    return shell_path.split("/")[-1]


def get_memory():
    mem_total = ""
    mem_available = ""
    with open("/proc/meminfo", "r") as mem_file:
        for pair in mem_file.read().split("\n"):
            if pair.split(":")[0] == "MemTotal":
                mem_total = pair.split(":")[1].replace("kB", "").strip()
            elif pair.split(":")[0] == "MemAvailable":
                mem_available = pair.split(":")[1].replace("kB", "").strip()
    return f"{int((int(mem_total) - int(mem_available)) / int(mem_total) * 100)}%"


def get_packages():
    def get_lines(cmd):
        packages = check_output([cmd], shell=True, text=True)
        num_pkgs = len(packages.split("\n")) - 1
        return str(num_pkgs)

    name = get_name()
    if name in ["Ubuntu", "Debian", "Linux Mint", "PopOS", "Raspbian"]:
        return get_lines("dpkg -l")
    elif name in [
        "Arch",
        "EndeavourOS",
        "Artix",
        "Manjaro",
        "ArcoLinux",
        "Archcraft",
        "Garuda",
    ]:
        return get_lines("pacman -Qq")
    elif name == "NixOS":
        return get_lines("nix-store -qR /run/current-system/sw ~/.nix-profile")
    elif name in [
        "Fedora",
        "CentOS",
        "SUSE",
        "openSUSE Tumbleweed",
        "openSUSE Leap",
        "RHEL",
    ]:
        return get_lines("rpm -qa")
    elif name == "Void":
        return get_lines("xbps-query -l")
    elif name in ["Gentoo", "ChromeOS"]:
        return get_lines("ls -d /var/db/pkg/*/*| cut -f5- -d/")
    else:
        return "0/0"
