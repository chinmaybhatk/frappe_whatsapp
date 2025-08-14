# Frappe WhatsApp with Calling

WhatsApp integration for Frappe Framework with voice and video calling capabilities using LiveKit.

## Features

### Original WhatsApp Features
- WhatsApp Cloud API integration
- Send and receive messages
- Template management
- Webhook handling
- Media support

### New Calling Features
- Voice and video calling through WhatsApp
- LiveKit integration for WebRTC
- Agent dashboard for call management
- Call session tracking and history
- MCP (Model Context Protocol) tools for AI integration
- Real-time call status updates
- Call recording support (optional)

## Installation

```bash
# Clone the repository
cd frappe-bench
bench get-app https://github.com/chinmaybhatk/frappe_whatsapp.git

# Install on your site
bench --site your-site.com install-app frappe_whatsapp
```

## LiveKit Setup

### 1. Install LiveKit Server

#### For Development (Docker):
```bash
docker run -d \
  --name livekit \
  -p 7880:7880 \
  -p 7881:7881 \
  -p 7882:7882/udp \
  livekit/livekit-server \
  --dev
```

#### For Production:
Follow the [LiveKit deployment guide](https://docs.livekit.io/realtime/self-hosting/deployment/)

### 2. Configure Site Settings

Add to your `site_config.json`:

```json
{
    "livekit_api_key": "your-api-key",
    "livekit_api_secret": "your-api-secret",
    "livekit_url": "ws://localhost:7880",
    "livekit_webhook_url": "https://your-site.com/api/method/frappe_whatsapp.calling.livekit_integration.webhook"
}
```

For production, use secure WebSocket (wss://) and configure proper API keys.

### 3. Configure LiveKit Webhooks

In your LiveKit configuration, set the webhook endpoint:
```yaml
webhook:
  urls:
    - https://your-site.com/api/method/frappe_whatsapp.calling.livekit_integration.webhook
```

## Usage

### Agent Dashboard

1. Navigate to **WhatsApp Agent Dashboard** in the Desk
2. Agents can:
   - Make outbound calls
   - Receive incoming calls
   - View active calls
   - Access call history
   - Toggle audio/video
   - Record calls (if configured)

### MCP Tools

The app includes MCP tools for AI integration:

```python
# Available MCP tools:
- initiate_whatsapp_call: Start a call with a customer
- end_whatsapp_call: End an active call
- get_active_calls: List all active calls
- get_call_participants: Get participants in a call
- get_call_history: Retrieve call history
- send_call_invite_message: Send WhatsApp message with call link
```

### API Usage

```python
# Initiate a call
import frappe

result = frappe.call(
    "frappe_whatsapp.calling.livekit_integration.create_call_session",
    customer_phone="+1234567890",
    call_type="voice"  # or "video"
)

# End a call
frappe.call(
    "frappe_whatsapp.calling.livekit_integration.end_call",
    call_session="CALL-2024-00001"
)
```

## Customer Experience

1. Customer receives a WhatsApp message with a call invitation link
2. Clicking the link opens a web-based call interface
3. No app installation required - works in mobile/desktop browsers
4. Automatic audio/video permissions handling
5. Simple controls for mute/unmute and end call

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   WhatsApp  │────▶│   Frappe    │────▶│   LiveKit   │
│   Customer  │     │   Backend   │     │   Server    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                     ▲
                           ▼                     │
                    ┌─────────────┐              │
                    │    Agent     │──────────────┘
                    │  Dashboard   │
                    └─────────────┘
```

## Security Considerations

1. **Authentication**: Agents must be logged in to Frappe
2. **Guest Access**: Customers join calls via secure tokens
3. **Encryption**: LiveKit provides end-to-end encryption
4. **Permissions**: Role-based access control for agents
5. **Token Expiry**: Call tokens expire after 24 hours

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check LiveKit server is running
   - Verify firewall allows ports 7880-7882
   - Ensure correct WebSocket URL in config

2. **No Audio/Video**
   - Check browser permissions
   - Verify HTTPS for production
   - Test with LiveKit's built-in diagnostics

3. **Webhook Errors**
   - Verify webhook URL is accessible
   - Check Frappe logs for errors
   - Ensure proper authentication

## Development

### Running Tests
```bash
bench --site your-site.com run-tests --app frappe_whatsapp
```

### MCP Testing
```bash
# Test MCP tools
bench --site your-site.com execute frappe_whatsapp.calling.mcp_tools.get_active_calls
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Credits

- Original frappe_whatsapp by [Shridhar Patil](https://github.com/shridarpatil)
- LiveKit integration added by contributors
- Built on [Frappe Framework](https://frappeframework.com)
- Powered by [LiveKit](https://livekit.io)

## Support

For issues and feature requests, please use the [GitHub Issues](https://github.com/chinmaybhatk/frappe_whatsapp/issues) page.
