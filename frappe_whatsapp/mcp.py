"""Frappe WhatsApp MCP Integration."""
import frappe
import frappe_mcp
from frappe_whatsapp.utils import calling
from frappe_whatsapp.utils import send_whatsapp_message
import json

# Create MCP instance
mcp = frappe_mcp.MCP("whatsapp-mcp")


@mcp.tool()
def send_message(to: str, message: str, template_name: str = None):
    """Send a WhatsApp message.
    
    Args:
        to: WhatsApp number to send message to
        message: Message content
        template_name: Optional template name to use
    
    Returns:
        dict: Response from WhatsApp API
    """
    try:
        response = send_whatsapp_message(
            number=to,
            message=message,
            template_name=template_name
        )
        return {
            "success": True,
            "message_id": response.get("messages", [{}])[0].get("id"),
            "status": "sent"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def make_voice_call(to_number: str):
    """Initiate a WhatsApp voice call.
    
    Args:
        to_number: WhatsApp number to call
    
    Returns:
        dict: Call initiation response
    """
    return calling.initiate_voice_call(to_number)


@mcp.tool()
def end_voice_call(call_id: str):
    """End an ongoing WhatsApp voice call.
    
    Args:
        call_id: ID of the call to end
    
    Returns:
        dict: Call termination response
    """
    return calling.end_call(call_id)


@mcp.tool()
def get_call_history(phone_number: str = None, limit: int = 20):
    """Get WhatsApp call history.
    
    Args:
        phone_number: Optional filter by phone number
        limit: Maximum number of records to return (default: 20)
    
    Returns:
        list: List of call records
    """
    return calling.get_call_history(phone_number, limit)


@mcp.tool()
def get_active_calls():
    """Get all currently active WhatsApp calls.
    
    Returns:
        list: List of active call records
    """
    return calling.get_active_calls()


@mcp.tool()
def get_message_history(phone_number: str = None, limit: int = 20):
    """Get WhatsApp message history.
    
    Args:
        phone_number: Optional filter by phone number
        limit: Maximum number of records to return (default: 20)
    
    Returns:
        list: List of message records
    """
    filters = {}
    if phone_number:
        filters["from"] = phone_number
    
    messages = frappe.get_all(
        "WhatsApp Message",
        filters=filters,
        fields=["name", "type", "from", "to", "message", "status", 
                "content_type", "creation"],
        order_by="creation desc",
        limit=limit
    )
    
    return messages


@mcp.tool()
def get_whatsapp_templates():
    """Get all approved WhatsApp message templates.
    
    Returns:
        list: List of approved templates
    """
    templates = frappe.get_all(
        "WhatsApp Templates",
        filters={"status": "APPROVED"},
        fields=["name", "template_name", "language", "category", "components"]
    )
    
    # Parse components JSON
    for template in templates:
        if template.get("components"):
            template["components"] = json.loads(template["components"])
    
    return templates


@mcp.tool()
def get_whatsapp_settings():
    """Get WhatsApp configuration settings.
    
    Returns:
        dict: WhatsApp settings (excluding sensitive data)
    """
    settings = frappe.get_doc("WhatsApp Settings", "WhatsApp Settings")
    
    return {
        "enabled": settings.enabled,
        "calling_enabled": settings.calling_enabled,
        "call_recording_enabled": settings.call_recording_enabled,
        "max_call_duration": settings.max_call_duration,
        "phone_id": settings.phone_id,
        "business_id": settings.business_id
    }


@mcp.tool()
def send_bulk_messages(recipient_list: str, message: str, template_name: str = None):
    """Send bulk WhatsApp messages.
    
    Args:
        recipient_list: Name of the recipient list
        message: Message content
        template_name: Optional template name to use
    
    Returns:
        dict: Bulk message sending response
    """
    try:
        # Create bulk message document
        bulk_doc = frappe.new_doc("Bulk WhatsApp Message")
        bulk_doc.recipient_list = recipient_list
        bulk_doc.message = message
        if template_name:
            bulk_doc.template = template_name
        bulk_doc.insert()
        bulk_doc.submit()
        
        return {
            "success": True,
            "bulk_message_id": bulk_doc.name,
            "status": "initiated"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Register the MCP endpoint
@mcp.register()
def handle_mcp():
    """MCP endpoint handler."""
    # Import any additional tool modules here if needed
    pass
