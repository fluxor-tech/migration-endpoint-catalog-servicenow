# Authentication and Permissions Notes

ServiceNow REST API behavior depends on authentication, roles, table ACLs, field ACLs, domain separation, and application/plugin availability.

Common authentication modes:

- Basic authentication
- OAuth 2.0
- Mutual TLS or gateway-mediated authentication where configured

## Practical Checks

- Confirm table ACLs for read/write/delete operations.
- Confirm field ACLs when response fields are unexpectedly missing.
- Confirm domain separation behavior before treating counts as complete.
- Confirm plugin/application availability for product-specific APIs.
- Use `sysparm_fields` for controlled extraction and smaller payloads.
- Use `sysparm_display_value` intentionally; raw values are usually better for mapping, display values are useful for reports.

## Identifiers

ServiceNow records are identified by `sys_id`. Human-readable numbers such as `INC0010001` are useful business keys but should not replace `sys_id` in relationship mapping.

