# Standard Library
from base64 import b64encode

# Third Party
import magic
from jinja2 import Template  # noqa

# Flowcard
from flowcard.component import Component

m = magic.Magic(flags=magic.MAGIC_MIME_TYPE)


class Title(Component):
    name = "title"
    aliases = ["header"]

    def __init__(self, text):
        super().__init__()
        self.text = text

    def to_html(self):
        return {"head": f"<title>{self.text}</title>", "body": f"<h1>{self.text}</h1>"}

    def to_markdown(self):
        return f"# {self.text}"


class Favicon(Component):
    name = "favicon"

    def __init__(self, image_data):
        super().__init__()
        self.base64 = b64encode(image_data).decode("ascii")
        self.mime = m.id_buffer(image_data)

    def to_html(self):
        return {
            "head": f"<link rel='icon' type='{self.mime}'  href='data:{self.mime};base64,{self.base64}'/>",
            "body": "",
        }

    def to_markdown(self):
        return ""


class Image(Component):
    name = "image"

    def __init__(self, image_data, width=None, height=None):
        super().__init__()
        self.base64 = b64encode(image_data).decode("ascii")
        self.mime = m.id_buffer(image_data)

    def to_html(self):
        return {
            "head": "",
            "body": f"<img type='{self.mime}'  src='data:{self.mime};base64,{self.base64}'/>",
        }

    def to_markdown(self):
        return f"<img type='{self.mime}'  src='data:{self.mime};base64,{self.base64}'/>"
