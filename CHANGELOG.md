# Changelog

## 2026-06-20

- Initialized ServiceNow endpoint catalog.
- Added curated core platform catalog with Table, Aggregate, Attachment, Import Set, Batch, Service Catalog, CMDB Instance, OAuth, and common table aliases.
- Added validation and CSV index tooling.
- Added NOTICE and LICENSE.
- Clarified that ServiceNow completeness requires instance-generated table/API catalogs.
- Added `tools/generate_table_catalog_from_instance.py` to generate concrete Table API endpoint aliases from `sys_db_object`.
- Added generated common table catalog with 350 concrete Table API aliases across 70 common ServiceNow tables.
- Added global duplicate endpoint ID validation.
- Added official REST API family catalog with 25 additional endpoints/families surfaced by the ServiceNow Developer reference.
- Added generated Zurich REST API family index with 121 official ServiceNow API families from the Developer reference.
