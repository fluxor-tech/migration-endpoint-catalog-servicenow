# ServiceNow Endpoint Catalog

Complete catalog of ServiceNow REST endpoint families used for platform integrations, reporting, automation, governance, operational support, and migrations.

ServiceNow exposes many APIs through product families and instance-specific tables. This catalog models both fixed endpoints and parameterized endpoint families such as the Table API. It is not an SDK and does not replace ServiceNow official documentation.

## Scope

Current scope:

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

## Coverage

The first version is a curated platform catalog rather than a generated OpenAPI dump. ServiceNow tables make the Table API effectively parameterized, so table coverage is represented through reusable endpoint families plus high-value table aliases.

Use `catalog/indexes/all-endpoints.csv` for spreadsheet review and filtering.

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

