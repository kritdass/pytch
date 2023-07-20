#!/usr/bin/env python3

from os import getlogin, walk, environ
from os.path import isfile
from subprocess import check_output, DEVNULL, CalledProcessError
from platform import release
from re import search

art_text = """

      
 __ _ 
/ _` |
\\__,_|
      

 _    
| |__ 
| '_ \\
|_.__/
      

    
 __ 
/ _|
\\__|
    

    _ 
 __| |
/ _` |
\\__,_|
      

     
 ___ 
/ -_)
\\___|
     

  __ 
 / _|
|  _|
|_|  
     

      
 __ _ 
/ _` |
\\__, |
|___/ 

 _    
| |_  
| ' \\ 
|_||_|
      

 _ 
(_)
| |
|_|
   

   _ 
  (_)
  | |
 _/ |
|__/ 

 _   
| |__
| / /
|_\\_\\
     

 _ 
| |
| |
|_|
   

       
 _ __  
| '  \\ 
|_|_|_|
       

      
 _ _  
| ' \\ 
|_||_|
      

     
 ___ 
/ _ \\
\\___/
     

      
 _ __ 
| '_ \\
| .__/
|_|   

      
 __ _ 
/ _` |
\\__, |
   |_|

     
 _ _ 
| '_|
|_|  
     

    
 ___
(_-<
/__/
    

 _   
| |_ 
|  _|
 \\__|
     

      
 _  _ 
| || |
 \\_,_|
      

     
__ __
\\ V /
 \\_/ 
     

        
__ __ __
\\ V  V /
 \\_/\\_/ 
        

     
__ __
\\ \\ /
/_\\_\\
     

      
 _  _ 
| || |
 \\_, |
 |__/ 

    
 ___
|_ /
/__|
    

   _   
  /_\\  
 / _ \\ 
/_/ \\_\\
       

 ___ 
| _ )
| _ \\
|___/
     

  ___ 
 / __|
| (__ 
 \\___|
      

 ___  
|   \\ 
| |) |
|___/ 
      

 ___ 
| __|
| _| 
|___|
     

 ___ 
| __|
| _| 
|_|  
     

  ___ 
 / __|
| (_ |
 \\___|
      

 _  _ 
| || |
| __ |
|_||_|
      

 ___ 
|_ _|
 | | 
|___|
     

    _ 
 _ | |
| || |
 \\__/ 
      

 _  __
| |/ /
| ' < 
|_|\\_\\
      

 _    
| |   
| |__ 
|____|
      

 __  __ 
|  \\/  |
| |\\/| |
|_|  |_|
        

 _  _ 
| \\| |
| .` |
|_|\\_|
      

  ___  
 / _ \\ 
| (_) |
 \\___/ 
       

 ___ 
| _ \\
|  _/
|_|  
     

  ___  
 / _ \\ 
| (_) |
 \\__\\_\\
       

 ___ 
| _ \\
|   /
|_|_\\
     

 ___ 
/ __|
\\__ \\
|___/
     

 _____ 
|_   _|
  | |  
  |_|  
       

 _   _ 
| | | |
| |_| |
 \\___/ 
       

__   __
\\ \\ / /
 \\ V / 
  \\_/  
       

__      __
\\ \\    / /
 \\ \\/\\/ / 
  \\_/\\_/  
          

__  __
\\ \\/ /
 >  < 
/_/\\_\\
      

__   __
\\ \\ / /
 \\ V / 
  |_|  
       

 ____
|_  /
 / / 
/___|
     

"""


def art(text):
    result = [""]
    art_letters = art_text.split("\n\n")
    for char in text:
        offset = 38 if char.isupper() else 96

        for index, line in enumerate(art_letters[ord(char) - offset].split("\n")[::-1]):
            try:
                result[index] += line
            except IndexError:
                result.append(line)

    return "\n".join(result[::-1])


def color(text, color):
    colors = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
    }
    return f"\033[{colors[color]}m{text}\033[0m"


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

    return "RHEL" if name.startswith("Red Hat") else name


def get_kernel():
    if "zen" in release():
        return release().split("-")[0] + "-zen"
    else:
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
        "openSUSE",
        "Mandriva",
        "Scientific",
        "RHEL",
    ]:
        return get_lines("rpm -qa")
    elif name == "Void":
        return get_lines("xbps-query -l")
    elif name in ["Gentoo", "ChromeOS"]:
        return get_lines("ls -d /var/db/pkg/*/*| cut -f5- -d/")
    else:
        return "0/0"


def main():
    attrs = [
        {"name": "user", "value": getlogin(), "icon": "", "color": "red"},
        {"name": "os", "value": get_name(), "icon": "", "color": "yellow"},
        {"name": "kernel", "value": get_kernel(), "icon": "", "color": "green"},
        {"name": "uptime", "value": get_uptime(), "icon": "", "color": "blue"},
        {"name": "shell", "value": get_shell(), "icon": "", "color": "magenta"},
        {"name": "pkgs", "value": get_packages(), "icon": "", "color": "red"},
        {"name": "memory", "value": get_memory(), "icon": "󰍛", "color": "cyan"},
    ]

    print(color(art(get_name()), "cyan"))

    name_width = max([len(attr["name"]) for attr in attrs])
    value_width = max([len(attr["value"]) for attr in attrs])
    gap = len(art(get_name()).split("\n")[-1]) - name_width - value_width - 8

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
