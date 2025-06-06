# Standard Library
from base64 import b64encode

# Third Party
import magic
from jinja2 import Template  # noqa

# Flowcard
from flowcard.component import Component

# Initialize magic for MIME type detection
m = magic.Magic(mime=True)


class Title(Component):
    name = "title"

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def to_html(self) -> dict[str, str]:
        return {"head": f"<title>{self.text}</title>", "body": f"<h1>{self.text}</h1>"}

    def to_markdown(self) -> str:
        return f"# {self.text}"


class Favicon(Component):
    name = "favicon"

    def __init__(self, image_data: bytes) -> None:
        super().__init__()
        self.base64 = b64encode(image_data).decode(encoding="ascii")
        self.mime = m.from_buffer(image_data)

    def to_html(self) -> dict[str, str]:
        return {
            "head": f"<link rel='icon' type='{self.mime}'  href='data:{self.mime};base64,{self.base64}'/>",
            "body": "",
        }

    def to_markdown(self) -> str:
        return ""


class Image(Component):
    name = "image"

    def __init__(self, image_data: bytes, width: int | None = None, height: int | None = None) -> None:
        super().__init__()
        self.base64 = b64encode(image_data).decode(encoding="ascii")
        self.mime = m.from_buffer(image_data)

    def to_html(self) -> dict[str, str]:
        return {
            "head": "",
            "body": f"<img type='{self.mime}'  src='data:{self.mime};base64,{self.base64}'/>",
        }

    def to_markdown(self) -> str:
        return f"<img type='{self.mime}'  src='data:{self.mime};base64,{self.base64}'/>"


class Header(Component):
    name = "header"

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def to_html(self) -> dict[str, str]:
        return {"head": "", "body": f"<h2>{self.text}</h2>"}

    def to_markdown(self) -> str:
        return f"## {self.text}"
