"""WhatsApp API endpoints."""
import frappe
from frappe_whatsapp.utils import calling
from frappe_whatsapp.utils import send_whatsapp_message


@frappe.whitelist()
def make_call(to_number):
    """API endpoint to make a WhatsApp call.
    
    Args:
        to_number: The WhatsApp number to call
    
    Returns:
        dict: Response from initiate_voice_call
    """
    return calling.initiate_voice_call(to_number)


@frappe.whitelist()
def end_call(call_id):
    """API endpoint to end a WhatsApp call.
    
    Args:
        call_id: The ID of the call to end
    
    Returns:
        dict: Response from end_call
    """
    return calling.end_call(call_id)


@frappe.whitelist()
def get_call_history(phone_number=None, limit=20):
    """API endpoint to get call history.
    
    Args:
        phone_number: Optional filter by phone number
        limit: Maximum number of records to return
    
    Returns:
        list: List of call records
    """
    return calling.get_call_history(phone_number, int(limit))


@frappe.whitelist()
def get_active_calls():
    """API endpoint to get active calls.
    
    Returns:
        list: List of active call records
    """
    return calling.get_active_calls()


@frappe.whitelist()
def send_message(to, message, template_name=None):
    """API endpoint to send a WhatsApp message.
    
    Args:
        to: WhatsApp number to send message to
        message: Message content
        template_name: Optional template name to use
    
    Returns:
        dict: Response from WhatsApp API
    """
    return send_whatsapp_message(
        number=to,
        message=message,
        template_name=template_name
    )
