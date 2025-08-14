# WhatsApp Calling Features

This document describes the WhatsApp calling functionality added to the frappe_whatsapp module.

## Features Added

### 1. WhatsApp Call DocType

A new DocType `WhatsApp Call` has been added to track voice calls:

- **Fields:**
  - Type (Incoming/Outgoing)
  - From Number
  - To Number
  - Status (initiated, ringing, answered, ended, missed, failed)
  - Call ID
  - Started At
  - Ended At
  - Duration (seconds)
  - Recording URL
  - Notes
  - Conversation ID
  - Metadata (JSON)

### 2. Calling Configuration

Added new fields to `WhatsApp Settings`:

- **Enable WhatsApp Calling**: Toggle to enable/disable calling functionality
- **Enable Call Recording**: Toggle to enable/disable call recording
- **Maximum Call Duration**: Set maximum allowed call duration in seconds

### 3. Webhook Enhancement

Updated the webhook handler to process call events:

```python
# Handles incoming call events
- Call initiation
- Call status updates (ringing, answered, ended, missed, failed)
- Call recordings (if enabled)
```

### 4. API Endpoints

New API endpoints for calling functionality:

#### Make a Call
```python
POST /api/method/frappe_whatsapp.api.make_call
{
    "to_number": "+1234567890"
}
```

#### End a Call
```python
POST /api/method/frappe_whatsapp.api.end_call
{
    "call_id": "CALL-123456"
}
```

#### Get Call History
```python
GET /api/method/frappe_whatsapp.api.get_call_history
?phone_number=+1234567890&limit=20
```

#### Get Active Calls
```python
GET /api/method/frappe_whatsapp.api.get_active_calls
```

### 5. Utility Functions

New utility functions in `frappe_whatsapp.utils.calling`:

- `initiate_voice_call(to_number, display_name=None)`
- `end_call(call_id)`
- `get_call_history(phone_number=None, limit=20)`
- `get_active_calls()`

## MCP (Model Context Protocol) Integration

### MCP Server

The frappe_whatsapp module now includes MCP server functionality with the following tools:

#### Available MCP Tools:

1. **send_message**: Send WhatsApp messages
2. **make_voice_call**: Initiate WhatsApp voice calls
3. **end_voice_call**: End ongoing calls
4. **get_call_history**: Retrieve call history
5. **get_active_calls**: Get currently active calls
6. **get_message_history**: Retrieve message history
7. **get_whatsapp_templates**: Get approved message templates
8. **get_whatsapp_settings**: Get WhatsApp configuration
9. **send_bulk_messages**: Send bulk messages

#### MCP Endpoint

The MCP server is available at:
```
http://<SITE_NAME:PORT>/api/method/frappe_whatsapp.mcp.handle_mcp
```

### Usage with AI Assistants

The MCP integration allows AI assistants like Claude to:
- Make and manage WhatsApp calls
- Send WhatsApp messages
- Access call and message history
- Manage bulk messaging campaigns

## Installation

1. Install the frappe-mcp package:
```bash
pip install frappe-mcp
```

2. Update your site:
```bash
bench --site <site-name> migrate
```

3. Configure WhatsApp Settings:
   - Enable WhatsApp integration
   - Enable calling functionality
   - Set up webhook URL in Meta/WhatsApp Business API

## Testing

Run the test suite:
```bash
bench --site <site-name> run-tests --app frappe_whatsapp
```

## Webhook Configuration

Ensure your WhatsApp webhook is configured to handle the following events:
- messages
- calls
- message_status
- call_status

## Security Considerations

1. All API endpoints require authentication
2. MCP endpoint can be configured with OAuth2 authentication
3. Call recordings are stored securely as File documents
4. Sensitive data like tokens are stored as password fields

## Limitations

1. Currently supports only voice calls (video calls not yet implemented)
2. Call recording depends on WhatsApp Business API support
3. Maximum call duration is configurable but depends on WhatsApp limits

## Future Enhancements

1. Video call support
2. Group call functionality
3. Call analytics and reporting
4. Integration with CRM modules
5. Call transcription support
