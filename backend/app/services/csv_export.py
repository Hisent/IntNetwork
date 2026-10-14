"""CSV für Excel (deutsch): UTF-8 mit BOM, Semikolon, Quoting per csv-Modul.

Formel-Injection: Namen, Freitexte und Fragetexte kommen von Teilnehmern bzw.
aus dem Editor. Excel/LibreOffice werten eine Zelle, die mit = + - @ (oder Tab/CR
davor) beginnt, als Formel aus — solche TEXTzellen bekommen ein ' vorangestellt
(OWASP "CSV Injection"). Zahlen bleiben Zahlen (sonst würde aus -5 der Text '-5)."""
import csv
import io

from fastapi.responses import Response

_FORMULA_START = ("=", "+", "-", "@", "\t", "\r")


def _cell(value) -> object:
    if value is None:
        return ""
    if isinstance(value, str) and value.startswith(_FORMULA_START):
        return "'" + value
    if isinstance(value, float):  # Dezimalkomma: Excel (DE) liest 4.2 sonst als Datum/Text
        return f"{value:.1f}".replace(".", ",")
    return value


def to_csv(rows: list[list]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter=";", quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
    writer.writerows([[_cell(v) for v in row] for row in rows])
    return "﻿" + buf.getvalue()


def csv_response(rows: list[list], filename: str) -> Response:
    return Response(content=to_csv(rows).encode("utf-8"), media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})
