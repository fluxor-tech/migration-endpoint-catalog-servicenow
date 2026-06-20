import csv
from pathlib import Path

import yaml


CATALOG_DIR = Path("catalog")
OUTPUT_DIR = CATALOG_DIR / "indexes"


def iter_endpoints():
    for path in sorted(CATALOG_DIR.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for endpoint in data["endpoints"]:
            yield {
                "catalog": path.name,
                "vendor": data["vendor"],
                "product": data["product"],
                "api_family": data["api_family"],
                "api_group": endpoint.get("api_group", ""),
                "id": endpoint["id"],
                "status": endpoint["status"],
                "method": endpoint["method"],
                "path": endpoint["path"],
                "summary": endpoint["summary"],
                "operation_category": endpoint["operation_category"],
                "use_cases": "; ".join(endpoint.get("use_cases", [])),
                "official_doc_url": endpoint["official_doc_url"],
            }


def main():
    rows = list(iter_endpoints())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / "all-endpoints.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    by_group = {}
    by_category = {}
    for row in rows:
        by_group[row["api_group"]] = by_group.get(row["api_group"], 0) + 1
        by_category[row["operation_category"]] = by_category.get(row["operation_category"], 0) + 1

    lines = [
        "# ServiceNow Endpoint Catalog Index",
        "",
        f"Total endpoints: {len(rows)}",
        "",
        "## By API Group",
        "",
        "| API Group | Endpoints |",
        "| --- | ---: |",
    ]
    for group, count in sorted(by_group.items()):
        lines.append(f"| {group} | {count} |")
    lines.extend(["", "## By Operation Category", "", "| Category | Endpoints |", "| --- | ---: |"])
    for category, count in sorted(by_category.items()):
        lines.append(f"| {category} | {count} |")
    lines.extend(["", "## Files", "", "- `all-endpoints.csv`: flat index for spreadsheet filtering.", "- `../servicenow-core-platform.yml`: curated ServiceNow platform catalog.", ""])
    (OUTPUT_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {csv_path} ({len(rows)} rows)")


if __name__ == "__main__":
    main()

