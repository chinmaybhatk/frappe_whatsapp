"""WhatsApp Calling Utilities."""
import frappe
import requests
import json
from datetime import datetime


def initiate_voice_call(to_number, display_name=None):
    """Initiate a WhatsApp voice call.
    
    Args:
        to_number: The WhatsApp number to call
        display_name: Optional display name for the caller
    
    Returns:
        dict: Response from WhatsApp API
    """
    settings = frappe.get_doc("WhatsApp Settings", "WhatsApp Settings")
    
    if not settings.calling_enabled:
        frappe.throw("WhatsApp calling is not enabled in settings")
    
    # Create call record
    call_doc = frappe.get_doc({
        "doctype": "WhatsApp Call",
        "type": "Outgoing",
        "to_number": to_number,
        "from_number": settings.phone_id,
        "status": "initiated"
    })
    call_doc.insert(ignore_permissions=True)
    
    # The actual call initiation will be handled by the document's after_insert method
    return {
        "success": True,
        "call_id": call_doc.name,
        "message": "Call initiated successfully"
    }


def end_call(call_id):
    """End an ongoing WhatsApp call.
    
    Args:
        call_id: The ID of the call to end
    
    Returns:
        dict: Response indicating success or failure
    """
    try:
        call_doc = frappe.get_doc("WhatsApp Call", call_id)
        call_doc.end_call()
        
        return {
            "success": True,
            "message": "Call ended successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


def get_call_history(phone_number=None, limit=20):
    """Get call history.
    
    Args:
        phone_number: Optional filter by phone number
        limit: Maximum number of records to return
    
    Returns:
        list: List of call records
    """
    filters = {}
    if phone_number:
        filters["from_number"] = phone_number
    
    calls = frappe.get_all(
        "WhatsApp Call",
        filters=filters,
        fields=["name", "type", "from_number", "to_number", "status", 
                "started_at", "ended_at", "duration"],
        order_by="creation desc",
        limit=limit
    )
    
    return calls


def get_active_calls():
    """Get all active calls.
    
    Returns:
        list: List of active call records
    """
    return frappe.get_all(
        "WhatsApp Call",
        filters={
            "status": ["in", ["initiated", "ringing", "answered"]]
        },
        fields=["name", "type", "from_number", "to_number", "status", "started_at"]
    )


@frappe.whitelist()
def make_call(to_number):
    """API endpoint to make a WhatsApp call.
    
    Args:
        to_number: The WhatsApp number to call
    
    Returns:
        dict: Response from initiate_voice_call
    """
    return initiate_voice_call(to_number)


@frappe.whitelist()
def terminate_call(call_id):
    """API endpoint to terminate a WhatsApp call.
    
    Args:
        call_id: The ID of the call to terminate
    
    Returns:
        dict: Response from end_call
    """
    return end_call(call_id)


@frappe.whitelist()
def get_calls(phone_number=None, limit=20):
    """API endpoint to get call history.
    
    Args:
        phone_number: Optional filter by phone number
        limit: Maximum number of records to return
    
    Returns:
        list: List of call records
    """
    return get_call_history(phone_number, int(limit))
