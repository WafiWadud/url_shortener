"""Url Shortner Frontend And Backend"""
from os.path import exists
from nicegui import ui
from random import randbytes
from base64 import b64encode


@ui.page("/app")
def app() -> None:
    input_field = ui.input(label="Enter A Url")
    link_label = ui.label(text="")

    def on_enter():
        shortened_link = makelink(input_field.value)
        link_label.set_text(shortened_link)
    input_field.on("keydown.enter", on_enter)
    link_label = ui.label(text="")


def makelink(link) -> str:
    name = b64encode(randbytes(6)).decode()
    content = ""
    if exists("urls.txt"):
        with open("urls.txt", "r") as file:
            content = file.read()
        if name in content:
            makelink(link)
        else:
            with open(__file__, "a") as file:
                file.writelines([f"@ui.page(\"/link/{name}\")", f"def {name}: ui.open({link})"])
            return name

    with open("urls.txt", "a") as file:
        file.write(name)
    makelink(link)
    return name


ui.run(title="Url Shortener")
