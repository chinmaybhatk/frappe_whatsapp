import frappe

def after_install():
    """Setup after app installation"""
    # Create WhatsApp Agent role if not exists
    if not frappe.db.exists("Role", "WhatsApp Agent"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "WhatsApp Agent",
            "desk_access": 1,
            "is_custom": 0
        }).insert(ignore_permissions=True)
    
    # Add LiveKit configuration to site_config.json hints
    print("\n" + "="*50)
    print("WhatsApp Calling Setup Instructions:")
    print("="*50)
    print("\nAdd the following to your site_config.json:")
    print('''
{
    "livekit_api_key": "your-api-key",
    "livekit_api_secret": "your-api-secret",
    "livekit_url": "ws://localhost:7880",
    "livekit_webhook_url": "https://your-site.com/api/method/frappe_whatsapp.calling.livekit_integration.webhook"
}
''')
    print("\nFor production, use a secure WebSocket URL (wss://)")
    print("\nTo start a local LiveKit server for testing:")
    print("docker run -d -p 7880:7880 -p 7881:7881 -p 7882:7882/udp livekit/livekit-server --dev")
    print("="*50 + "\n")
    
    frappe.db.commit()
