"""Url Shortner Frontend And Backend"""
from os.path import exists
from nicegui import ui
from random import randbytes
from base64 import b64encode


@ui.page("/app")
def app() -> None:
    """
    Summary: Represents the app page.

    Explanation:
    This function represents the app page. It creates an input field and a label for displaying a shortened link. When the user enters a URL and presses enter, it generates a shortened link using the `makelink` function and displays it in the label.

    Args:
    - None

    Returns:
    - None

    Examples:
    - None
    """

    input_field = ui.input(label="Enter A Url")
    link_label = ui.label(text="")

    def on_enter() -> None:
        """
        Summary: Handles the event when the user presses enter in the input field.

        Explanation:
        This function is called when the user presses enter in the input field. It generates a shortened link using the `makelink` function with the value of the input field, and sets the text of the link label to the shortened link.

        Args:
        - None

        Returns:
        - None

        Examples:
        - None
        """

        shortened_link: str = makelink(link=input_field.value)
        link_label.set_text(text=shortened_link)

    input_field.on(type="keydown.enter", handler=on_enter)
    link_label = ui.label(text="")


def writelink(name: str, link: str) -> str:
    """
    Summary: Writes a link to a file and updates the UI.

    Explanation:
    This function takes a name and a link as input and writes them to a file named "urls.txt". It also updates the UI by adding a new page and a corresponding function that opens the provided link when accessed. Finally, it opens the "/link/" page in the UI. The function returns the name of the link.

    Args:
    - name (str): The key of the link.
    - link (str): The URL to be associated with the link.

    Returns:
    - str: The key of the link.

    Examples:
    - None
    """

    if exists("urls.txt"):
        with open("urls.txt", "a") as file:
            file.write(f"{name} {link}")
        with open(__file__, "a") as file:
            file.writelines(
                [f"\n@ui.page(\"/link/{name}\")\n", f"def {name}(): ui.open(\"{link}\")"])
            ui.open("./link/")
        return name
    else:
        with open("urls.txt", "w"):
            file.write("")


def makelink(link: str) -> str:
    """
    Summary: Generates a unique key for a link and writes it to a file.

    Explanation:
    This function takes a link as input and generates a unique key for it using base64 encoding and random bytes. It checks if the key already exists in the "urls.txt" file. If it does, it recursively calls itself to generate a new key. If the key is unique, it writes the key and link to the file using the `writelink` function.

    Args:
    - link (str): The URL to be associated with the link.

    Returns:
    - str: The generated key for the link.

    Examples:
    - None
    """

    name: str = b64encode(randbytes(6)).decode()
    content: str = ""
    if exists("urls.txt"):
        with open("urls.txt", "r") as file:
            content = file.read()
        if name in content:
            return makelink(link=link)  # Return the recursive call
        else:
            return writelink(name=name, link=link)

    else:
        with open("urls.txt", "w") as file:
            file.write("")
        return writelink(name=name, link=link)


@ui.page("/link")
def link() -> None:
    """
    Summary: Represents the link page.

    Explanation:
    This function represents the link page. It reads the content of the "urls.txt" file and displays it in a label on the UI.

    Args:
    - None

    Returns:
    - None

    Examples:
    - None
    """

    if exists("urls.txt"):
        with open("urls.txt", "r") as file:
            content: str = file.read()
            ui.label(text=content)
    else:
        with open("urls.txt", "w") as file:
            file.write("")


ui.run(title="Url Shortener")
