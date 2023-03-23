import logging

from jinja2 import Template
from flowcard.component import Component, Container


class Flowcard(Container):
    def __init__(self, title=None, **kwargs):
        super().__init__()
        self.components = []
        self.html_template = Template(
            """<!DOCTYPE html>
            <html>
                <head>
                <title>{{ title }}</title>
                </head>
                <body>
                {{ content }}
                </body>
            </html>"""
        )
        self.markdown_template = Template(
            """{{ content }}"""
        )
        self.kwargs = kwargs
        if "content" in self.kwargs:
            logging.warning("Arg content given in arguments, it is a reserved argument. Automatically removed.")
            self.kwargs.pop("content")

    def to_html(self):
        content = "\n".join([component.to_html() for component in self.components])
        self.kwargs.update({"content": content})
        return self.html_template.render(**self.kwargs)

    def to_markdown(self):
        content = "\n".join([component.to_markdown() for component in self.components])
        self.kwargs.update({"content": content})
        return self.markdown_template.render(**self.kwargs)


class Title(Component):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def to_html(self):
        return f"<h1>{self.text}</h1>"

    def to_markdown(self):
        return f"# {self.text}"




