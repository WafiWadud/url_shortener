"""Url Shortner Frontend And Backend"""
from os import listdir
from nicegui import ui
from random import randbytes
from base64 import b64encode
@ui.page("/app")
def app() -> None:
    input_field = ui.input(label="Enter A Url")
    link_label = ui.label(text="")
    def on_enter():
        shortened_link = makelink(input_field.value)
        link_label.set(shortened_link)
    input_field.on("keydown.enter", on_enter)
    link_label = ui.label(text="")

def makelink(link) -> str:
    name = b64encode(randbytes(6)).decode()
    if name and name + ".py" in listdir():
        return
    with open(file=name + ".py", mode="w") as file:
        file.writelines(f"from nicegui import ui\n@ui.page(\"{name}\")\ndef {name}: ui.open(\"{link}\")")
    return name

ui.run(title="Url Shortener")