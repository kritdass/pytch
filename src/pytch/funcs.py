from os import walk, environ
from os.path import isfile
from platform import release
from sys import platform
from subprocess import check_output, DEVNULL, CalledProcessError
from re import search, findall, sub, split
from pytch.art import art_dict

def get_output(cmd):
    return check_output([cmd], shell=True, text=True, stderr=DEVNULL)


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
    try:
        distro = art_dict[distro.lower()]
    except KeyError:
        distro = art_dict["default"]

    length = max(
        [len(sub(r"\$\{c[1-6]\}", "", line)) for line in distro["ascii"].splitlines()]
    )

    segments = split(r"\$\{c[1-6]\}", distro["ascii"])[1:]
    colors = [
        int(pattern[3]) - 1 for pattern in findall(r"\$\{c[1-6]\}", distro["ascii"])
    ]

    result = ""
    for i in range(len(segments)):
        result += color(segments[i], distro["colors"][colors[i]])

    min_length = 45
    if length < min_length:
        spacer = " " * ((min_length - length) // 2)
        result = "\n".join([spacer + line + spacer for line in result.splitlines()])
        length = min_length

    return {"art": result, "length": length}


def get_name():
    def get_lsb_release():
        try:
            return get_output("lsb_release -a")
        except (OSError, CalledProcessError):
            return ""

    def get_distro_release():
        for _, _, files in walk("/etc"):
            for release_file in files:
                if search("(-|_)(release|version)", release_file):
                    with open(release_file, "r") as file:
                        for pair in file.read().splitlines():
                            if pair.split("=")[0] == "DISTRIB_ID":
                                return pair.split("=")[1]
        return ""

    name = ""
    if platform == "darwin":
        name = "Darwin"
    elif isfile("/etc/os-release") or isfile("/usr/lib/os-release"):
        release_file = (
            "/etc/os-release" if isfile("/etc/os-release") else "/usr/lib/os-release"
        )
        with open(release_file, "r") as os_release:
            os_release = os_release.read().splitlines()
            for pair in os_release:
                if pair.split("=")[0] == "NAME":
                    name = pair.split("=")[1]
    elif get_lsb_release():
        lsb_release = get_lsb_release().splitlines()
        for pair in lsb_release:
            if pair.split(":")[0] == "Distributor ID":
                name = pair.split(":")[1].strip()
    elif get_distro_release():
        name = get_distro_release()

    return "RHEL" if name.startswith("Red Hat") else name.replace('"', "")


def get_kernel():
    return release().split("-")[0].strip()


def get_uptime():
    seconds = 0

    if get_name() in ["Darwin", "FreeBSD"]:
        boot = get_output("sysctl -n kern.boottime")
        boot = search(r"sec = (\d+)", boot).group(1)
        now = get_output("date +%s")
        seconds = int(now) - int(boot)
    else:
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

    if get_name() == "Darwin":
        mem_total = int(get_output("sysctl -n hw.memsize"))
        vm_stat = get_output("vm_stat").splitlines()
        page_size = search(
            r"^Mach Virtual Memory Statistics: \(page size of (\d+) bytes\)$",
            vm_stat[0],
        ).group(1)
        mem = {}
        for line in vm_stat[1:]:
            mem[line.split(":")[0]] = int(float(line.split(":")[1].strip()))
        mem_available = (
            mem["Pages wired down"] + mem["Pages active"] + mem["Pages inactive"]
        ) * int(page_size)
    elif get_name() == "FreeBSD":
        mem_total = int(get_output("sysctl -n hw.physmem")) / 1024
        page_size = int(get_output("sysctl -n hw.pagesize"))
        mem_available = int(get_output("sysctl -n vm.stats.vm.v_free_count")) * page_size / 1024
    else:
        with open("/proc/meminfo", "r") as mem_file:
            for pair in mem_file.read().splitlines():
                if pair.split(":")[0] == "MemTotal":
                    mem_total = pair.split(":")[1].replace("kB", "").strip()
                elif pair.split(":")[0] == "MemAvailable":
                    mem_available = pair.split(":")[1].replace("kB", "").strip()

    return f"{int((int(mem_total) - int(mem_available)) * 100 / int(mem_total))}%"

def get_packages():
    def get_lines(cmd):
        packages = get_output(cmd)
        num_pkgs = len(packages.splitlines())
        return str(num_pkgs)

    packages = []

    name = get_name()
    if name in ["Ubuntu", "Debian", "Linux Mint", "PopOS", "Raspbian"]:
        packages.append(f"{get_lines('dpkg -l')} (deb)")
    elif name in [
        "Arch",
        "EndeavourOS",
        "Artix",
        "Manjaro",
        "ArcoLinux",
        "Archcraft",
        "Garuda",
    ]:
        packages.append(f"{get_lines('pacman -Qq')} (pcmn)")
    elif name in [
        "Fedora",
        "CentOS",
        "SUSE",
        "openSUSE Tumbleweed",
        "openSUSE Leap",
        "RHEL",
    ]:
        packages.append(f"{get_lines('rpm -qa')} (rpm)")
    elif name == "Void":
        packages.append(f"{get_lines('xbps-query -l')} (xbps)")
    elif name in ["Gentoo", "ChromeOS"]:
        packages.append(f"{get_lines('ls -d /var/db/pkg/*/*| cut -f5- -d/')} (portage)")
    elif name == "NixOS":
        packages.append(
            f"{get_lines('nix-store -qR /run/current-system/sw ~/.nix-profile')} (nix)"
        )
    elif name == "FreeBSD":
        packages.append(f"{get_lines('pkg info -q')} (pkg)")

    if name != "NixOS":
        if name == "Darwin":
            try:
                packages.append(
                    f"{get_lines('nix-store -qR /run/current-system/sw ~/.nix-profile')} (nix)"
                )
            except:
                pass
        else:
            try:
                packages.append(
                    f"{get_lines('nix-store -qR /nix/var/nix/profiles/default ~/.nix-profile ')} (nix)"
                )
            except:
                pass

    try:
        packages.append(f"{get_lines('brew list')} (brew)")
    except:
        pass

    if not packages:
        packages.append("0/0")

    return packages
