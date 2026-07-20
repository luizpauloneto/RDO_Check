from __future__ import annotations

from pathlib import Path
from typing import List

import cv2


class TableRowSplitter:
    """
    Divide a tabela de mão de obra em uma imagem por colaborador.
    """

    def split(
        self,
        image_path: Path,
        output_dir: Path,
    ) -> List[Path]:

        image = cv2.imread(str(image_path))

        if image is None:
            raise RuntimeError(f"Imagem inválida: {image_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        inv = cv2.threshold(
            gray,
            180,
            255,
            cv2.THRESH_BINARY_INV,
        )[1]

        horizontal = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (80, 1),
        )

        lines = cv2.morphologyEx(
            inv,
            cv2.MORPH_OPEN,
            horizontal,
        )

        contours, _ = cv2.findContours(
            lines,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        ys = []

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > image.shape[1] * 0.60:
                ys.append(y)

        ys = sorted(set(ys))

        output_dir.mkdir(parents=True, exist_ok=True)

        rows: List[Path] = []

        for idx in range(len(ys) - 1):
            top = ys[idx]
            bottom = ys[idx + 1]

            if bottom - top < 25:
                continue

            crop = image[top:bottom, :]

            name = f"{image_path.stem}_row_{idx+1:03}.png"
            path = output_dir / name

            cv2.imwrite(str(path), crop)
            rows.append(path)

        return rows
