# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
from datetime import datetime


class WhatsAppCall(Document):
    def validate(self):
        """Validate the call document."""
        if not self.from_number and not self.to_number:
            frappe.throw("Either 'From Number' or 'To Number' is required")
        
        if self.status not in ["initiated", "ringing", "answered", "ended", "missed", "failed"]:
            frappe.throw("Invalid call status")
    
    def after_insert(self):
        """Actions after inserting the call record."""
        if self.type == "Outgoing" and self.status == "initiated":
            self.initiate_call()
    
    def initiate_call(self):
        """Initiate a WhatsApp voice call."""
        settings = frappe.get_doc("WhatsApp Settings", "WhatsApp Settings")
        
        if not settings.calling_enabled:
            frappe.throw("WhatsApp calling is not enabled in settings")
        
        token = settings.get_password("token")
        phone_number_id = settings.phone_id
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # WhatsApp Cloud API endpoint for initiating calls
        url = f"{settings.url}/{settings.version}/{phone_number_id}/messages"
        
        # Call initiation payload
        payload = {
            "messaging_product": "whatsapp",
            "to": self.to_number,
            "type": "interactive",
            "interactive": {
                "type": "call",
                "action": {
                    "name": "voice_call",
                    "parameters": {
                        "display_phone_number": self.from_number or phone_number_id,
                        "call_id": self.name
                    }
                }
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            
            if response.status_code == 200:
                self.call_id = response_data.get("messages", [{}])[0].get("id")
                self.status = "ringing"
                self.save(ignore_permissions=True)
                frappe.msgprint("Call initiated successfully")
            else:
                error_msg = response_data.get("error", {}).get("message", "Unknown error")
                frappe.throw(f"Failed to initiate call: {error_msg}")
                
        except Exception as e:
            frappe.log_error(f"WhatsApp Call Error: {str(e)}", "WhatsApp Call")
            frappe.throw(f"Error initiating call: {str(e)}")
    
    def end_call(self):
        """End an ongoing WhatsApp call."""
        if self.status not in ["answered", "ringing"]:
            frappe.throw("Call is not active")
        
        self.status = "ended"
        self.ended_at = datetime.now()
        
        if self.started_at and self.ended_at:
            duration = (self.ended_at - self.started_at).total_seconds()
            self.duration = int(duration)
        
        self.save(ignore_permissions=True)
        frappe.msgprint("Call ended")
    
    @frappe.whitelist()
    def update_call_status(self, status, **kwargs):
        """Update call status from webhook."""
        self.status = status
        
        if status == "answered":
            self.started_at = datetime.now()
        elif status in ["ended", "missed", "failed"]:
            self.ended_at = datetime.now()
            if self.started_at and self.ended_at:
                duration = (self.ended_at - self.started_at).total_seconds()
                self.duration = int(duration)
        
        # Update any additional fields from webhook
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.save(ignore_permissions=True)
