# ServiceNow Endpoint Catalog

Catalog of ServiceNow REST endpoint families used for platform integrations, reporting, automation, governance, operational support, and migrations.

ServiceNow exposes many APIs through product families and instance-specific tables. This catalog models both fixed endpoints and parameterized endpoint families such as the Table API. It is not an SDK and does not replace ServiceNow official documentation.

## Scope

Current curated scope:

- Core Platform APIs
- Table API
- Aggregate API
- Attachment API
- Import Set API
- Batch API
- Service Catalog API
- CMDB Instance API
- User, group, role, and identity-related table endpoints
- Common ITSM table endpoints

Out of scope for the first pass:

- Instance-specific Scripted REST APIs
- Store application APIs not present in a base platform
- Legacy SOAP APIs
- Custom table endpoints that only exist in a customer instance

## Repository Layout

```text
catalog/
  indexes/
    README.md
    all-endpoints.csv
  servicenow-core-platform.yml
  servicenow-common-tables.yml
examples/
  requests/
  responses/
notes/
  auth-and-permissions.md
  use-cases.md
schemas/
  endpoint.schema.json
sources/
  official-docs.md
tools/
  export_catalog_indexes.py
  validate_catalog.py
```

## Coverage Model

ServiceNow does not have a single static public OpenAPI file that represents every endpoint available in every customer instance. The effective endpoint universe depends on:

- Platform release
- Installed plugins and applications
- Custom tables
- Scripted REST APIs
- ACLs and roles
- Domain separation

For that reason, this repository has two layers:

- `catalog/servicenow-core-platform.yml`: curated core endpoint families and high-value table aliases.
- `catalog/servicenow-common-tables.yml`: concrete Table API aliases for common platform/application tables.
- Instance-generated catalogs: produced from a real instance using `tools/generate_table_catalog_from_instance.py`.

Use `catalog/indexes/all-endpoints.csv` for spreadsheet review and filtering.

Current committed coverage:

| Catalog | Endpoints |
| --- | ---: |
| Core platform endpoint families | 46 |
| Common table aliases | 350 |
| **Total** | **396** |

## Generate A Real Instance Table Catalog

Set credentials for a ServiceNow instance and generate concrete Table API endpoint aliases from `sys_db_object`:

```bash
set SERVICENOW_INSTANCE=example
set SERVICENOW_USER=admin
set SERVICENOW_PASSWORD=...
python tools/generate_table_catalog_from_instance.py
python tools/export_catalog_indexes.py
```

This produces `catalog/servicenow-instance-tables.yml`, which is the correct way to expand beyond the curated core list.

## Regenerate Common Table Aliases

```bash
python tools/generate_common_table_catalog.py
python tools/export_catalog_indexes.py
```

## Status Values

- `candidate`: identified from official documentation or stable platform convention, not yet reviewed.
- `reviewed`: checked against official documentation and catalog classification is clear.
- `validated`: tested against a real ServiceNow instance with documented behavior.
- `deprecated`: retained only for historical context.

## Validation

```bash
python tools/validate_catalog.py
python tools/export_catalog_indexes.py
```
