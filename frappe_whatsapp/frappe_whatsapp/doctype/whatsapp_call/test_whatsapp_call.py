# Copyright (c) 2024, Frappe Technologies and Contributors
# See license.txt

import frappe
import unittest

class TestWhatsAppCall(unittest.TestCase):
    def setUp(self):
        # Create test WhatsApp Settings if not exists
        if not frappe.db.exists("WhatsApp Settings", "WhatsApp Settings"):
            settings = frappe.new_doc("WhatsApp Settings")
            settings.calling_enabled = 1
            settings.phone_id = "1234567890"
            settings.token = "test_token"
            settings.url = "https://graph.facebook.com"
            settings.version = "v17.0"
            settings.save(ignore_permissions=True)
    
    def test_call_creation(self):
        call = frappe.new_doc("WhatsApp Call")
        call.type = "Outgoing"
        call.from_number = "1234567890"
        call.to_number = "0987654321"
        call.status = "initiated"
        call.insert()
        
        self.assertEqual(call.type, "Outgoing")
        self.assertEqual(call.status, "initiated")
    
    def test_call_validation(self):
        call = frappe.new_doc("WhatsApp Call")
        call.type = "Incoming"
        call.status = "invalid_status"
        
        with self.assertRaises(frappe.ValidationError):
            call.insert()
    
    def test_call_status_update(self):
        call = frappe.new_doc("WhatsApp Call")
        call.type = "Incoming"
        call.from_number = "1234567890"
        call.to_number = "0987654321"
        call.status = "ringing"
        call.insert()
        
        call.update_call_status("answered")
        self.assertEqual(call.status, "answered")
        self.assertIsNotNone(call.started_at)
