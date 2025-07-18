# Rosy AI API Quick Reference

Quick reference guide for the most common API operations.

## 🔐 Authentication

### Get Access Token
```bash
curl -X POST "http://localhost:8000/api/auth/passwordless" \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username"}'
```

### Verify Token
```bash
curl -X POST "http://localhost:8000/api/auth/verify" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 💬 Chat Operations

### List All Chats
```bash
curl -X GET "http://localhost:8000/api/chats/list_chats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create New Chat
```bash
curl -X POST "http://localhost:8000/api/chats/create_chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My New Chat"}'
```

### Send Message
```bash
curl -X POST "http://localhost:8000/api/chats/CHAT_ID/send_message" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello, AI!"}'
```

### Get Chat History
```bash
curl -X GET "http://localhost:8000/api/chats/CHAT_ID/history" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Delete Chat
```bash
curl -X DELETE "http://localhost:8000/api/chats/CHAT_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🏥 Health Checks

### App Health
```bash
curl -X GET "http://localhost:8000/health"
```

### Chat Service Health
```bash
curl -X GET "http://localhost:8000/api/chats/health"
```

## 🔧 TypeScript Quick Examples

### Basic Setup
```typescript
const API_BASE = 'http://localhost:8000';
const TOKEN = 'your_access_token';

const headers = {
  'Authorization': `Bearer ${TOKEN}`,
  'Content-Type': 'application/json'
};
```

### Send Message
```typescript
async function sendMessage(chatId: number, content: string) {
  const response = await fetch(`${API_BASE}/api/chats/${chatId}/send_message`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ content })
  });
  return response.json();
}
```

### Get Chat History
```typescript
async function getChatHistory(chatId: number) {
  const response = await fetch(`${API_BASE}/api/chats/${chatId}/history`, {
    headers: { 'Authorization': `Bearer ${TOKEN}` }
  });
  return response.json();
}
```

## 📋 Common Response Formats

### Success Response
```json
{
  "content": "AI response here",
  "message_id": 123,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```

### Chat Object
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Chat Title",
  "thread_id": "abc-123-def-456",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "is_deleted": false
}
```

## 🚨 Common Error Codes

- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (chat/message doesn't exist)
- `422` - Validation Error (invalid request data)
- `500` - Internal Server Error

## 💡 Tips

1. **Always include Authorization header** for protected endpoints
2. **Use Content-Type: application/json** for POST requests
3. **Handle errors gracefully** - check response status
4. **Store tokens securely** - they expire after 30 minutes
5. **Use chat IDs** from the list_chats response

## 🔗 Full Documentation

- [Complete API Documentation](API_DOCUMENTATION.md)
- [Interactive Swagger UI](http://localhost:8000/docs)
- [ReDoc Documentation](http://localhost:8000/redoc) 