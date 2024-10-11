import os
from menu_tda.menu import Menu
import minecraft_launcher_lib as minecraft
import subprocess

RUN = "Run"
ALLVERSION = "All versions"
INSTALLEDVERSIONS = "Installed versions"
CHANGENAME = "Change name"
INSTALLFORGE = "Forge versions"
EXIT = "Exit"

minecraft_path = "../data"


def InstallForgeVersion(menu):
    version = minecraft.forge.find_forge_version(menu.forge_version())
    if not version:
        return
    minecraft.forge.install_forge_version(version, minecraft_path)


def InstalledVersions(menu):
    menu.select_version(minecraft.utils.get_installed_versions(minecraft_path))


def Allversions(menu):
    menu.select_version(minecraft.utils.get_version_list())


def ChangeName(menu):
    menu.change_name()


def Run(menu):
    if not os.path.exists(minecraft_path + "/versions/" + menu.version):
        print(f"Version {menu.version} is not installed, wait...")
        minecraft.install.install_minecraft_version(menu.version, minecraft_path)

    minecraft_command = minecraft.command.get_minecraft_command(
        menu.version, minecraft_path, menu.player
    )
    subprocess.run(minecraft_command)


def Main():
    menu = Menu(minecraft.utils.get_latest_version()["release"])
    active = None
    while active != EXIT:
        active = menu.main_menu()
        if active == RUN:
            Run(menu)
        elif active == INSTALLEDVERSIONS:
            InstalledVersions(menu)
        elif active == ALLVERSION:
            Allversions(menu)
        elif active == CHANGENAME:
            ChangeName(menu)
        elif active == INSTALLFORGE:
            InstallForgeVersion(menu)


if __name__ == "__main__":
    Main()
