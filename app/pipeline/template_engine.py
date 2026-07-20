from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RegionTemplate:
    name: str
    x1: float
    y1: float
    x2: float
    y2: float
    prompt: str | None = None

    def __post_init__(self):
        if self.prompt is None:
            # por padrão usa o mesmo nome da região
            self.prompt = self.name

    @property
    def bbox(self):
        """
        Compatibilidade com o SmartCropper.
        Retorna (x, y, largura, altura)
        """
        return (
            self.x1,
            self.y1,
            self.x2 - self.x1,
            self.y2 - self.y1,
        )


class TemplateEngine:
    """
    Templates por tipo de página.

    Coordenadas em percentual (0.0 a 1.0).
    """

    def __init__(self):

        self.templates = {

            "rdo": [
                RegionTemplate("header",        0.03, 0.02, 0.97, 0.16),
                RegionTemplate("employees",     0.03, 0.16, 0.97, 0.52),
                RegionTemplate("activities",    0.03, 0.52, 0.97, 0.76),
                RegionTemplate("observations",  0.03, 0.76, 0.97, 0.86),
                RegionTemplate("signatures",    0.03, 0.86, 0.97, 0.98),
            ],

            "fotografico": [
                RegionTemplate("header",        0.03, 0.02, 0.97, 0.12),
                RegionTemplate("photos",        0.03, 0.12, 0.97, 0.84),
                RegionTemplate("captions",      0.03, 0.84, 0.97, 0.98),
            ],

            "lista_presenca": [
                RegionTemplate("header",        0.03, 0.02, 0.97, 0.12),
                RegionTemplate("attendance",    0.03, 0.12, 0.97, 0.98),
            ],

            "unknown": [
                RegionTemplate("document",      0.02, 0.02, 0.98, 0.98),
            ],
        }

    def get(self, page_type: str):
        return self.templates.get(page_type, self.templates["unknown"])
