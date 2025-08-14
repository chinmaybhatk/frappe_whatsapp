"""WhatsApp utility functions."""
import frappe
import requests
import json
from frappe.utils import now_datetime, add_to_date


def send_whatsapp_message(number, message, reference_doctype=None, reference_name=None,
                         media_link=None, media_caption=None, media_filename=None,
                         template_name=None, language_code="en", custom_data=None,
                         message_type="text"):
    """Send WhatsApp message."""
    settings = frappe.get_doc(
        "WhatsApp Settings", "WhatsApp Settings"
    )
    token = settings.get_password("token")
    headers = {
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    your_phone_number_id = settings.phone_id

    if not template_name:
        message_data = format_message_json(
            message_type, number, message, media_link, media_caption,
            media_filename
        )
    else:
        message_data, template_name, modified_data = get_template_info(
            template_name,
            language_code,
            custom_data
        )
        message_data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                },
                "components": message_data
            }
        }
    try:
        response = requests.post(
            f"{settings.url}/{settings.version}/{your_phone_number_id}/messages",
            json=message_data,
            headers=headers
        )
        if response.ok:
            messages = response.json().get('messages')
            if messages:
                id = messages[0].get("id")
                frappe.get_doc({
                    "doctype": "WhatsApp Message",
                    "message": str(template_name) + str(modified_data) if template_name else str(message),
                    "to": number,
                    "message_id": id,
                    "type": "Outgoing",
                    "reference_doctype": reference_doctype,
                    "reference_name": reference_name,
                    "content_type": message_type
                }).save(ignore_permissions=True)
                frappe.msgprint("WhatsApp message sent")
        else:
            frappe.throw("An error occurred")
    except Exception as e:
        frappe.throw(f"An error occurred: {e}")
    return response.json()


def format_message_json(message_type, number, message, media_link, media_caption, media_filename):
    """Format message JSON based on type."""
    if message_type == "text":
        return {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "text",
            "text": {
                "body": message
            }
        }
    elif message_type in ["image", "audio", "video", "document"]:
        media_data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": message_type,
            message_type: {
                "link": media_link
            }
        }
        if media_caption and message_type in ["image", "video", "document"]:
            media_data[message_type]["caption"] = media_caption
        if media_filename and message_type == "document":
            media_data[message_type]["filename"] = media_filename
        return media_data
    else:
        frappe.throw(f"Unsupported message type: {message_type}")


def get_template_info(template_name, language_code, data):
    """Get template information."""
    # Implementation details for template handling
    # This is a simplified version - actual implementation would fetch from WhatsApp Templates doctype
    return [], template_name, data
