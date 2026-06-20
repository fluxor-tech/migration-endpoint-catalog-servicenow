import json
import re
from datetime import date
from pathlib import Path

import yaml


SOURCE = Path("sources/servicenow-rest-api-index-zurich.json")
OUTPUT = Path("catalog/servicenow-official-api-families.yml")


def clean_html(value):
    value = re.sub(r"<[^>]+>", "", value or "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def slug_from_link(link):
    return link.rstrip("/").split("/")[-1]


def main():
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    items = payload["result"]["items"]
    families = []
    for item in items:
        families.append(
            {
                "id": slug_from_link(item["link"]),
                "title": item["title"],
                "description": clean_html(item.get("description", "")),
                "official_doc_url": item["link"],
                "status": "official_indexed",
            }
        )

    data = {
        "vendor": "ServiceNow",
        "product": "ServiceNow Platform",
        "api_family": "ServiceNow REST API Family Index",
        "official_docs": {
            "root": "https://developer.servicenow.com/dev.do#!/reference/api/zurich/rest",
            "source": "sources/servicenow-rest-api-index-zurich.json",
        },
        "catalog_status": "active",
        "release": "zurich",
        "last_reviewed": date.today().isoformat(),
        "generation": {
            "source": "official_developer_reference_api_index",
            "api_family_count": len(families),
        },
        "api_families": families,
    }
    OUTPUT.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False, width=140), encoding="utf-8")
    print(f"Generated {len(families)} API families into {OUTPUT}")


if __name__ == "__main__":
    main()
