import logging
import os
from enum import Enum
import textwrap

from smalld import SmallD

logging.basicConfig(
    level=logging.DEBUG if os.environ.get("MCM_DEBUG") else logging.INFO
)


class Option(Enum):
    sub_command = 1
    sub_command_group = 2
    string = 3


smalld = SmallD.v8()

application_id = None
macros = {}

commands = [
    {
        "name": "macro",
        "description": "Macro management",
        "options": [
            {
                "name": "add",
                "description": "Add macro",
                "type": Option.sub_command.value,
                "options": [
                    {
                        "name": "name",
                        "description": "Macro name",
                        "type": Option.string.value,
                    },
                    {
                        "name": "text",
                        "description": "Macro text",
                        "type": Option.string.value,
                    },
                ],
            },
            {
                "name": "delete",
                "description": "Delete macro",
                "type": Option.sub_command.value,
                "options": [
                    {
                        "name": "name",
                        "description": "Macro name",
                        "type": Option.string.value,
                    }
                ],
            },
            {
                "name": "list",
                "description": "List macros",
                "type": Option.sub_command.value,
            },
        ],
    }
]


@smalld.on_ready
def on_ready(json):
    global application_id
    application_id = json.application.id

    for command in commands:
        smalld.post(f"/applications/{application_id}/commands", command)


def send_response(interaction, message):
    url = f"interactions/{interaction.id}/{interaction.token}/callback"

    smalld.post(url, {"type": 4, "data": {"content": message}})


def add_macro(guild_id, name, text):
    url = f"applications/{application_id}/guilds/{guild_id}/commands"

    smalld.post(
        url,
        {
            "name": name,
            "description": textwrap.shorten(text, width=20, placeholder="..."),
        },
    )

    guild_macros = macros.get(guild_id, {})
    guild_macros[name] = text
    macros[guild_id] = guild_macros


def options_to_dict(opts):
    return {o.name: o.value for o in opts}


@smalld.on_interaction_create
def on_command(interaction):
    command = interaction.data
    guild_id = interaction.guild_id

    if command.name == "macro":
        for subcommand in command.options:
            if subcommand.name == "add":
                add_macro(guild_id, **options_to_dict(subcommand.options))
                send_response(interaction, "Macro added.")
    elif command.name in (guild_macros := macros.get(guild_id, {})):
        send_response(interaction, guild_macros[command.name])


smalld.run()
