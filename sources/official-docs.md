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

## Review Rules

1. Every endpoint must include an `official_doc_url`.
2. Prefer ServiceNow official documentation over secondary docs or blog posts.
3. Mark endpoints as `candidate` until their classification and permission model have been reviewed.
4. Mark endpoints as `validated` only after instance testing has confirmed request/response behavior.
5. Custom tables and Scripted REST APIs should be added in separate overlays or tenant-specific catalogs.

