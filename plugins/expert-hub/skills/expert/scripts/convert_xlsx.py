"""Explicit XLSX sheet export; preserve Excel row ids and reject uncached formula values."""
import argparse
import csv
import json
import sys
from pathlib import Path

from qa_core import digest


def convert(source, sheet, destination, header_row=1):
    from openpyxl import load_workbook
    source, destination = Path(source), Path(destination)
    if destination.exists() or destination.with_suffix(destination.suffix + ".meta.json").exists():
        raise FileExistsError("Choose a new CSV destination")
    if source.suffix.lower() != ".xlsx" or header_row < 1:
        raise ValueError("Use an .xlsx file and a positive header row")
    formulas = load_workbook(source, read_only=True, data_only=False)
    cached = load_workbook(source, read_only=True, data_only=True)
    try:
        if sheet not in cached.sheetnames:
            raise ValueError("Sheet not found; available: " + ", ".join(cached.sheetnames))
        fs, vs = formulas[sheet], cached[sheet]
        values = list(vs.iter_rows(values_only=True))
        if len(values) < header_row:
            raise ValueError("Header row beyond worksheet")
        headers = [str(v) if v is not None else "" for v in values[header_row - 1]]
        if any(not h for h in headers) or len(headers) != len(set(headers)) or "__source_excel_row" in headers:
            raise ValueError("Headers must be nonempty and unique, without __source_excel_row")
        formula_count = 0
        for row in fs.iter_rows(min_row=header_row + 1):
            for cell in row:
                if cell.data_type == "f":
                    formula_count += 1
                    if values[cell.row - 1][cell.column - 1] is None:
                        raise ValueError(f"Uncached formula at {cell.coordinate}; recalculate and save in Excel before export")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["__source_excel_row", *headers])
            for row_number, row in enumerate(values[header_row:], header_row + 1):
                writer.writerow([row_number, *row])
        metadata = {"source": str(source.resolve()), "sha256": digest(source), "sheet": sheet, "header_row": header_row, "rows": len(values) - header_row, "formula_cells": formula_count, "warnings": ["Cached formula values may be stale even when present; confirm workbook recalculation date.", "Hidden rows/columns included. Number formats and display units are not inferred."]}
        destination.with_suffix(destination.suffix + ".meta.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        return metadata
    finally:
        formulas.close()
        cached.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument("--sheet", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--header-row", type=int, default=1)
    args = parser.parse_args()
    try:
        print(json.dumps(convert(args.file, args.sheet, args.out, args.header_row), ensure_ascii=False))
    except (ImportError, ValueError, OSError) as exc:
        sys.stderr.write(str(exc) + "\n")
        raise SystemExit(2)
