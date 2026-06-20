import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import yaml


OUTPUT = Path("catalog/servicenow-instance-tables.yml")


def required_env(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def request_json(url, user, password):
    token = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Basic {token}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_tables(instance, user, password):
    base = f"https://{instance}.service-now.com"
    fields = "name,label,super_class,sys_scope,access"
    query = "nameISNOTEMPTY"
    params = urllib.parse.urlencode(
        {
            "sysparm_query": query,
            "sysparm_fields": fields,
            "sysparm_limit": "10000",
            "sysparm_exclude_reference_link": "true",
        }
    )
    url = f"{base}/api/now/table/sys_db_object?{params}"
    payload = request_json(url, user, password)
    return payload.get("result", [])


def endpoint_id(prefix, table_name):
    safe = table_name.replace("_", "-").lower()
    return f"{prefix}-{safe}"


def table_endpoints(table):
    name = table["name"]
    label = table.get("label") or name
    common = {
        "status": "validated",
        "api_group": "Instance Table API",
        "auth": {"types": ["basic", "oauth_2_0"]},
        "official_doc_url": "https://developer.servicenow.com/dev.do#!/reference/api",
        "notes": [
            f"Generated from sys_db_object for table {name}.",
            f"Label: {label}",
        ],
    }
    return [
        {
            **common,
            "id": endpoint_id("table-query", name),
            "method": "GET",
            "path": f"/api/now/table/{name}",
            "summary": f"Query {label} records.",
            "operation_category": "read",
            "use_cases": [f"{label} lookup, extraction, reporting, and validation"],
            "permissions": [f"{name} read ACL"],
        },
        {
            **common,
            "id": endpoint_id("table-create", name),
            "method": "POST",
            "path": f"/api/now/table/{name}",
            "summary": f"Create a {label} record.",
            "operation_category": "write",
            "use_cases": [f"{label} creation and integration writes"],
            "permissions": [f"{name} create ACL"],
        },
        {
            **common,
            "id": endpoint_id("table-read", name),
            "method": "GET",
            "path": f"/api/now/table/{name}/{{sysId}}",
            "summary": f"Read one {label} record by sys_id.",
            "operation_category": "read",
            "use_cases": [f"{label} record lookup and validation"],
            "permissions": [f"{name} read ACL"],
        },
        {
            **common,
            "id": endpoint_id("table-update", name),
            "method": "PATCH",
            "path": f"/api/now/table/{name}/{{sysId}}",
            "summary": f"Update one {label} record by sys_id.",
            "operation_category": "write",
            "use_cases": [f"{label} selective updates and backfills"],
            "permissions": [f"{name} write ACL"],
        },
        {
            **common,
            "id": endpoint_id("table-delete", name),
            "method": "DELETE",
            "path": f"/api/now/table/{name}/{{sysId}}",
            "summary": f"Delete one {label} record by sys_id.",
            "operation_category": "delete",
            "use_cases": [f"{label} cleanup where permitted"],
            "permissions": [f"{name} delete ACL"],
        },
    ]


def main():
    instance = required_env("SERVICENOW_INSTANCE")
    user = required_env("SERVICENOW_USER")
    password = required_env("SERVICENOW_PASSWORD")
    tables = sorted(fetch_tables(instance, user, password), key=lambda row: row["name"])
    endpoints = []
    for table in tables:
        endpoints.extend(table_endpoints(table))

    data = {
        "vendor": "ServiceNow",
        "product": f"ServiceNow Instance: {instance}",
        "api_family": "ServiceNow Table API",
        "base_url_template": f"https://{instance}.service-now.com",
        "official_docs": {
            "root": "https://developer.servicenow.com/dev.do#!/reference/api",
            "instance_source": "/api/now/table/sys_db_object",
        },
        "catalog_status": "active",
        "last_reviewed": date.today().isoformat(),
        "generation": {
            "source": "servicenow_instance_sys_db_object",
            "table_count": len(tables),
            "endpoint_count": len(endpoints),
        },
        "endpoints": endpoints,
    }
    OUTPUT.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False, width=140), encoding="utf-8")
    print(f"Generated {len(endpoints)} endpoints from {len(tables)} tables into {OUTPUT}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
