"""Url Shortner Frontend And Backend"""
from os import listdir
from nicegui import ui
from random import randbytes
@ui.page("/app")
def app() -> None:
    input_field = ui.input(label="Enter A Url")
    link_label = ui.label(text="")
    def on_enter():
        shortened_link = makelink(input_field.get())
        link_label.set(shortened_link)
    input_field.on("keydown.enter", on_enter)

def makelink(link) -> str:
    name = randbytes(6)
    if name and name + ".py" in listdir():
        return
    with open(file=name, mode="w") as file:
        file.writelines(f"from nicegui import ui\n@ui.page(\"{name}\")\ndef {name}: ui.open(\"{link}\")")
    return name