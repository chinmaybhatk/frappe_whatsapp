import frappe

def get_context(context):
    """Context for WhatsApp call page"""
    context.no_cache = 1
    context.show_sidebar = False
    
    # Get room name from query parameters
    room_name = frappe.form_dict.get('room')
    
    if room_name:
        # Verify room exists and is active
        call_session = frappe.db.get_value(
            "WhatsApp Call Session",
            {"room_name": room_name, "status": ["in", ["Waiting", "Connected"]]},
            ["name", "call_type"],
            as_dict=True
        )
        
        if call_session:
            context.room_name = room_name
            context.call_type = call_session.call_type
        else:
            context.error = "Invalid or expired call session"
    else:
        context.error = "No room specified"
    
    return context
