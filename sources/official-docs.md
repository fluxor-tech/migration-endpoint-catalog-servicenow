# Official ServiceNow Documentation Sources

Primary sources for this catalog:

- ServiceNow Developer API reference: <https://developer.servicenow.com/dev.do#!/reference/api>
- ServiceNow product documentation: <https://www.servicenow.com/docs/>

API families covered in the initial curated catalog:

- Table API
- Aggregate API
- Attachment API
- Import Set API
- Batch API
- Service Catalog API
- CMDB Instance API
- OAuth token endpoint
- Common table endpoints for ITSM, CMDB, identity, metadata, audit, journal, knowledge, and attachments
- Common platform/application table aliases generated from the documented Table API pattern
- Additional REST API families surfaced by the ServiceNow Developer API reference bundle
- Full Zurich REST API family index from `https://developer.servicenow.com/api/snc/api_index_data?release=zurich&apiType=rest`

## Review Rules

1. Every endpoint must include an `official_doc_url`.
2. Prefer ServiceNow official documentation over secondary docs or blog posts.
3. Mark endpoints as `candidate` until their classification and permission model have been reviewed.
4. Mark endpoints as `validated` only after instance testing has confirmed request/response behavior.
5. Custom tables and Scripted REST APIs should be added in separate overlays or tenant-specific catalogs.

## Completeness Note

A static ServiceNow catalog cannot be globally complete for every customer because table endpoints are generated from instance schema and Scripted REST APIs can be custom-built. Use `tools/generate_table_catalog_from_instance.py` against a real instance to produce a concrete table endpoint catalog for that environment.
