from datetime import date
from pathlib import Path

import yaml


OUTPUT = Path("catalog/servicenow-common-tables.yml")

# Common ServiceNow platform/application tables exposed through the Table API.
# The generic Table API still supports any readable table; this file expands
# high-value documented platform tables into concrete endpoint aliases.
TABLES = [
    ("alm_asset", "Asset"),
    ("alm_hardware", "Hardware Asset"),
    ("alm_license", "Software License Asset"),
    ("ast_contract", "Contract"),
    ("change_task", "Change Task"),
    ("cmdb_ci_appl", "Application CI"),
    ("cmdb_ci_business_app", "Business Application CI"),
    ("cmdb_ci_computer", "Computer CI"),
    ("cmdb_ci_database", "Database CI"),
    ("cmdb_ci_ip_router", "IP Router CI"),
    ("cmdb_ci_linux_server", "Linux Server CI"),
    ("cmdb_ci_netgear", "Network Gear CI"),
    ("cmdb_ci_service", "Service CI"),
    ("cmdb_ci_server", "Server CI"),
    ("cmdb_ci_win_server", "Windows Server CI"),
    ("cmdb_model", "CMDB Model"),
    ("cmdb_model_category", "CMDB Model Category"),
    ("cmn_cost_center", "Cost Center"),
    ("cmn_department", "Department"),
    ("cmn_location", "Location"),
    ("cmn_schedule", "Schedule"),
    ("core_company", "Company"),
    ("contract_sla", "SLA Definition"),
    ("discovery_device_history", "Discovery Device History"),
    ("em_alert", "Event Management Alert"),
    ("em_event", "Event Management Event"),
    ("hr_case", "HR Case"),
    ("kb_category", "Knowledge Category"),
    ("kb_knowledge_base", "Knowledge Base"),
    ("kb_use", "Knowledge Use"),
    ("metric_instance", "Metric Instance"),
    ("problem_task", "Problem Task"),
    ("sc_cat_item", "Catalog Item"),
    ("sc_category", "Catalog Category"),
    ("sc_catalog", "Catalog"),
    ("sc_item_option", "Catalog Item Option"),
    ("sc_item_option_mtom", "Catalog Item Option Link"),
    ("sc_item_produced_record", "Catalog Produced Record"),
    ("sc_multi_row_question_answer", "Multi-Row Variable Set Answer"),
    ("sc_task_sla", "Catalog Task SLA"),
    ("sla", "SLA"),
    ("sn_customerservice_case", "Customer Service Case"),
    ("sys_app", "Application"),
    ("sys_attachment_doc", "Attachment Document Chunk"),
    ("sys_audit_delete", "Deleted Record Audit"),
    ("sys_choice_set", "Choice Set"),
    ("sys_db_view", "Database View"),
    ("sys_documentation", "Field Documentation"),
    ("sys_email", "Email"),
    ("sys_email_log", "Email Log"),
    ("sys_group_has_role", "Group Role Assignment"),
    ("sys_history_line", "History Line"),
    ("sys_history_set", "History Set"),
    ("sys_metadata", "Metadata"),
    ("sys_properties", "System Property"),
    ("sys_security_acl", "Access Control"),
    ("sys_ui_action", "UI Action"),
    ("sys_ui_form", "Form"),
    ("sys_ui_list", "List Layout"),
    ("sys_ui_policy", "UI Policy"),
    ("sys_update_set", "Update Set"),
    ("sys_update_xml", "Customer Update"),
    ("sys_user_delegate", "User Delegate"),
    ("sys_user_preference", "User Preference"),
    ("sys_user_token", "User Token"),
    ("sysapproval_approver", "Approval"),
    ("sysapproval_group", "Approval Group"),
    ("task_ci", "Task CI Relationship"),
    ("task_sla", "Task SLA"),
    ("u_task", "Custom Task Pattern"),
]


def slug(value):
    return value.replace("_", "-").lower()


def endpoints_for(table, label):
    base = {
        "status": "reviewed",
        "api_group": "Common Table API Alias",
        "auth": {"types": ["basic", "oauth_2_0"]},
        "official_doc_url": "https://developer.servicenow.com/dev.do#!/reference/api",
        "notes": [
            "Concrete alias for the documented ServiceNow Table API.",
            f"Table: {table}",
        ],
    }
    return [
        {
            **base,
            "id": f"table-query-{slug(table)}",
            "method": "GET",
            "path": f"/api/now/table/{table}",
            "summary": f"Query {label} records.",
            "operation_category": "read",
            "use_cases": [f"{label} lookup, extraction, reporting, and validation"],
            "permissions": [f"{table} read ACL"],
        },
        {
            **base,
            "id": f"table-create-{slug(table)}",
            "method": "POST",
            "path": f"/api/now/table/{table}",
            "summary": f"Create a {label} record.",
            "operation_category": "write",
            "use_cases": [f"{label} creation and integration writes"],
            "permissions": [f"{table} create ACL"],
        },
        {
            **base,
            "id": f"table-read-{slug(table)}",
            "method": "GET",
            "path": f"/api/now/table/{table}/{{sysId}}",
            "summary": f"Read one {label} record by sys_id.",
            "operation_category": "read",
            "use_cases": [f"{label} record lookup and validation"],
            "permissions": [f"{table} read ACL"],
        },
        {
            **base,
            "id": f"table-update-{slug(table)}",
            "method": "PATCH",
            "path": f"/api/now/table/{table}/{{sysId}}",
            "summary": f"Update one {label} record by sys_id.",
            "operation_category": "write",
            "use_cases": [f"{label} selective updates and backfills"],
            "permissions": [f"{table} write ACL"],
        },
        {
            **base,
            "id": f"table-delete-{slug(table)}",
            "method": "DELETE",
            "path": f"/api/now/table/{table}/{{sysId}}",
            "summary": f"Delete one {label} record by sys_id.",
            "operation_category": "delete",
            "use_cases": [f"{label} cleanup where permitted"],
            "permissions": [f"{table} delete ACL"],
        },
    ]


def main():
    endpoints = []
    for table, label in sorted(TABLES):
        endpoints.extend(endpoints_for(table, label))

    data = {
        "vendor": "ServiceNow",
        "product": "ServiceNow Platform",
        "api_family": "ServiceNow Table API - Common Table Aliases",
        "base_url_template": "https://{instance}.service-now.com",
        "official_docs": {
            "root": "https://developer.servicenow.com/dev.do#!/reference/api",
            "table_api": "https://developer.servicenow.com/dev.do#!/reference/api",
        },
        "catalog_status": "active",
        "last_reviewed": date.today().isoformat(),
        "generation": {
            "source": "curated_common_tables",
            "table_count": len(TABLES),
            "endpoint_count": len(endpoints),
        },
        "endpoints": endpoints,
    }
    OUTPUT.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False, width=140), encoding="utf-8")
    print(f"Generated {len(endpoints)} endpoints from {len(TABLES)} common tables into {OUTPUT}")


if __name__ == "__main__":
    main()
