"""Url Shortner Frontend And Backend"""
from os.path import exists
from nicegui import ui
from random import choices
from threading import Lock

lock = Lock()


@ui.page("/app")
def app() -> None:
    with ui.row(justify='center', align='center'):
        with ui.column(justify='center', align='center'):
            input_field = ui.input(label="Enter A Url")
            link_label = ui.label(text="")

            def on_enter() -> None:
                shortened_link: str = makelink(link=input_field.value)
                link_label.set_text(text=shortened_link)

            input_field.on(type="keydown.enter", handler=on_enter)


def writelink(name: str, link: str) -> str:
    with lock:
        mode: str = "a" if exists("urls.txt") else "w"
        with open("urls.txt", mode) as file:
            file.write(f"{name} {link}\n")
    return f"{name}"


def makelink(link: str) -> str:
    validletters: list[str] = ["A", "a", "B", "b", "C", "c", "D", "d"]
    name: str = ''.join(choices(validletters, k=6))
    content: str = ""
    if not exists("urls.txt"):
        return writelink(name=name, link=link)
    with open("urls.txt", "r") as file:
        content = file.read()
    return (
        makelink(link=link)
        if name in content
        else writelink(name=name, link=link)
    )


@ui.page("/link/{shortened_link}")
def redirect_to_link(shortened_link: str) -> None:
    if exists("urls.txt"):
        with open("urls.txt", "r") as file:
            for line in file:
                name, link = line.split()
                if name == shortened_link:
                    match link:
                        case _ if link.startswith("www.") and not link.startswith("https://"):
                            link = "https://" + link
                        case _ if link.startswith("https://") and not link.startswith("https://www."):
                            link = link.replace("https://", "https://www.")
                        case _ if not link.startswith("www.") and not link.startswith("https://"):
                            link = "https://www." + link
                    with ui.row(justify='center', align='center'):
                        with ui.column(justify='center', align='center'):
                            ui.button("goto link?",
                                      on_click=lambda: ui.open(f'{link}'))


ui.run(title="Url Shortener", tailwind=False)
