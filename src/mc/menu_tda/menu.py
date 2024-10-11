import json
import inquirer
import os
from pprint import pprint
import uuid

player_path = "../data/session_data/player.json"
version_path = "../data/session_data/version.json"
minecraft_directory = "../data/"
choices = (
    "Run",
    "All versions",
    "Installed versions",
    "Forge versions",
    "Change name",
    "Exit",
)


def get_version(mc_version, change):
    if os.path.exists(version_path) and not change:
        with open(version_path, "r") as archivo:
            json_string = archivo.read()
        return json.loads(json_string)["version"]

    version = {"version": mc_version}
    json_string = json.dumps(version, indent=2)
    with open(version_path, "w") as archivo:
        archivo.write(json_string)

    return version["version"]


def insert_name(change):
    if os.path.exists(player_path) and not change:
        with open(player_path, "r") as file:
            json_string = file.read()
            return json.loads(json_string)

    questions = [inquirer.Text("name", message="Input your Minecraft name")]

    answers = inquirer.prompt(questions)

    if not answers:
        pprint("ERROR!")
        exit(1)

    if os.path.exists(player_path):
        os.remove(player_path)

    data = {"username": answers["name"], "uuid": str(uuid.uuid4()), "token": ""}

    json_string = json.dumps(data, indent=2)
    with open(player_path, "w") as archivo:
        archivo.write(json_string)
    return data


class Menu:
    def __init__(self, last_version):
        self.player = insert_name(False)
        self.version = get_version(last_version, False)

    def user_data_exist(self):
        return os.path.exists(player_path)

    def version_data_exist(self):
        return os.path.exists(version_path)

    def forge_version(self):

        questions = [
            inquirer.Text("version", message="Write the forge version?"),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            return None

        return answers["version"]

    def change_name(self):
        self.player = insert_name(True)

    def select_version(self, versions):
        list = [dc["id"] for dc in versions]
        questions = [
            inquirer.List(
                "version",
                message="Select a installed Minecraft version",
                choices=list,
            ),
            inquirer.Confirm("continue", message="Should I continue", default=True),
        ]
        answers = inquirer.prompt(questions)
        if not answers or not answers["continue"]:
            return

        self.version = get_version(answers["version"], True)

    def main_menu(self):
        questions = [
            inquirer.List("option", message="Select a option", choices=choices)
        ]
        answer = inquirer.prompt(questions)
        if not answer:
            exit(1)

        return answer["option"]
