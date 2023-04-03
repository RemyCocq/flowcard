import logging
from pathlib import Path
from typing import Union

from component import Container
from jinja2 import Template

from flowcard.base import Favicon, Image, Title


class Flowcard(Container):
    available_components = {}

    def __init__(self, **kwargs):
        super().__init__()
        self.register([Title, Favicon, Image])
        self.components = []
        self.html_template = Template(
            """<!DOCTYPE html>
            <html>
                <head>
                {{ head }}
                </head>
                <body>
                {{ body }}
                </body>
            </html>"""
        )
        self.markdown_template = Template("""{{ content }}""")
        self.kwargs = kwargs
        if "content" in self.kwargs:
            logging.warning(
                "Arg content given in arguments, it is a reserved argument. Automatically removed."
            )
            self.kwargs.pop("content")

    def to_html(self):
        head = "\n".join(
            (_component.to_html()["head"] for _component in self.components)
        )
        body = "\n".join(
            (_component.to_html()["body"] for _component in self.components)
        )
        self.kwargs.update({"head": head})
        self.kwargs.update({"body": body})
        return self.html_template.render(**self.kwargs)

    def to_markdown(self):
        content = "\n".join(
            [_component.to_markdown() for _component in self.components]
        )
        self.kwargs.update({"content": content})
        return self.markdown_template.render(**self.kwargs)

    def save(self, filepath: Union[Path, str], extension: Union[None, str] = None):
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if extension is None:
            extension = filepath.suffix
            if extension:
                extension = extension[1:]
        if extension not in ["html", "md"]:
            raise ValueError(
                "Please give a valid format to save in filename. Either give the argument 'extension' a value in ['html', 'md'], or give your filepath an valid extension between '.html' and '.md'."
            )
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w") as file:
            if extension == "html":
                file.write(self.to_html())
            elif extension == "md":
                file.write(self.to_markdown())

    @classmethod
    def register(cls, components):
        def add_component_factory(_component):
            def add_component(self, *args, **kwargs):
                self.components.append(_component(*args, **kwargs))

            return add_component

        for _component in components:
            setattr(cls, _component.name, add_component_factory(_component))

            if "aliases" in _component.__dict__:
                for alias in _component.aliases:
                    setattr(cls, alias, add_component_factory(_component))


if __name__ == "__main__":
    fl = Flowcard()
    fl.title("test title")

    with open("favicon.ico", "rb") as image:
        fl.favicon(image.read())

    with open("favicon.png", "rb") as image:
        fl.image(image.read())

    fl.save("test.html")
    fl.save("test.md")
