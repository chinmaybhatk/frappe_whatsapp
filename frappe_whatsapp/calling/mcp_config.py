"""MCP configuration for WhatsApp calling"""
import frappe
from frappe_whatsapp.calling.mcp_tools import mcp

# Configure MCP server info
mcp.server_info = {
    "name": "whatsapp-calling-mcp",
    "version": "1.0.0",
    "description": "MCP server for WhatsApp calling functionality in Frappe"
}

# Register the MCP endpoint in Frappe
def get_mcp_config():
    """Return MCP configuration for WhatsApp calling"""
    return {
        "name": "WhatsApp Calling MCP",
        "endpoint": "/api/method/frappe_whatsapp.calling.mcp_tools.handle_whatsapp_calling_mcp",
        "description": "MCP tools for managing WhatsApp calls",
        "tools": [
            {
                "name": "initiate_whatsapp_call",
                "description": "Initiate a WhatsApp call to a customer"
            },
            {
                "name": "end_whatsapp_call",
                "description": "End an active WhatsApp call"
            },
            {
                "name": "get_active_calls",
                "description": "Get list of all active WhatsApp calls"
            },
            {
                "name": "get_call_participants",
                "description": "Get list of participants in a call room"
            },
            {
                "name": "get_call_history",
                "description": "Get call history for a specific phone number or all calls"
            },
            {
                "name": "send_call_invite_message",
                "description": "Send a WhatsApp message with call invite link"
            }
        ]
    }
