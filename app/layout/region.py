from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Region:
    """
    Representa uma região encontrada em uma página.
    """

    page: int = 0

    kind: str = "UNKNOWN"

    x: int = 0

    y: int = 0

    width: int = 0

    height: int = 0

    confidence: float = 1.0

    image: str = ""

    # =====================================================

    @property
    def left(self) -> int:

        return self.x

    @property
    def top(self) -> int:

        return self.y

    @property
    def right(self) -> int:

        return self.x + self.width

    @property
    def bottom(self) -> int:

        return self.y + self.height

    # =====================================================

    @property
    def area(self) -> int:

        return self.width * self.height

    # =====================================================

    def to_dict(self):

        return {

            "page": self.page,

            "kind": self.kind,

            "x": self.x,

            "y": self.y,

            "width": self.width,

            "height": self.height,

            "confidence": self.confidence,

            "image": self.image

        }

    # =====================================================

    def __str__(self):

        return (

            f"{self.kind} "

            f"({self.x},{self.y}) "

            f"{self.width}x{self.height}"

        )