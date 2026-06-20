import json
from pathlib import Path

import yaml


REQUIRED_ROOT = {"vendor", "product", "api_family", "base_url_template", "official_docs", "catalog_status", "last_reviewed", "endpoints"}
REQUIRED_ENDPOINT = {"id", "status", "method", "path", "summary", "operation_category", "use_cases", "permissions", "official_doc_url"}


def main():
    json.loads(Path("schemas/endpoint.schema.json").read_text(encoding="utf-8"))
    total = 0
    family_total = 0
    global_ids = {}
    for path in sorted(Path("catalog").glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if "api_families" in data:
            ids = [family["id"] for family in data["api_families"]]
            if len(ids) != len(set(ids)):
                raise SystemExit(f"{path}: duplicate api family ids")
            expected = data.get("generation", {}).get("api_family_count")
            if expected is not None and expected != len(ids):
                raise SystemExit(f"{path}: generation.api_family_count={expected}, actual={len(ids)}")
            family_total += len(ids)
            print(f"{path}: {len(ids)} API families")
            continue
        missing = REQUIRED_ROOT - set(data)
        if missing:
            raise SystemExit(f"{path}: missing root keys {sorted(missing)}")
        ids = []
        for endpoint in data["endpoints"]:
            missing_endpoint = REQUIRED_ENDPOINT - set(endpoint)
            if missing_endpoint:
                raise SystemExit(f"{path}:{endpoint.get('id')}: missing {sorted(missing_endpoint)}")
            ids.append(endpoint["id"])
            if endpoint["id"] in global_ids:
                raise SystemExit(f"duplicate endpoint id across catalogs: {endpoint['id']} in {path} and {global_ids[endpoint['id']]}")
            global_ids[endpoint["id"]] = path
        if len(ids) != len(set(ids)):
            raise SystemExit(f"{path}: duplicate endpoint ids")
        expected = data.get("generation", {}).get("endpoint_count")
        if expected is not None and expected != len(ids):
            raise SystemExit(f"{path}: generation.endpoint_count={expected}, actual={len(ids)}")
        total += len(ids)
        print(f"{path}: {len(ids)} endpoints")
    print(f"total: {total} endpoints")
    print(f"api families: {family_total}")


if __name__ == "__main__":
    main()
