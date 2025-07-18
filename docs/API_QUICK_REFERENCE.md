# Rosy AI API Quick Reference

Quick reference guide for the most common API operations.

## 🔐 Authentication

### Get Access Token (Passwordless)
```bash
curl -X POST "http://localhost:8000/api/auth/passwordless" \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username"}'
```

### Register User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password",
    "email": "your_email@example.com"
  }'
```

### Login User
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"
```

### Get Current User
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Logout
```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer YOUR_TOKEN"
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
curl -X POST "http://localhost:8000/api/chats/send_message?chat_id=CHAT_ID" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello, AI!"}'
```

### Get Chat Messages
```bash
curl -X GET "http://localhost:8000/api/chats/get_chat_messages?chat_id=CHAT_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Edit Chat Title
```bash
curl -X PUT "http://localhost:8000/api/chats/edit_chat_title?chat_id=CHAT_ID&title=Updated%20Title" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Delete Chat
```bash
curl -X DELETE "http://localhost:8000/api/chats/CHAT_ID/delete_chat" \
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

### Authenticate (Passwordless)
```typescript
async function authenticate(username: string) {
  const response = await fetch(`${API_BASE}/api/auth/passwordless`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username })
  });
  return response.json();
}
```

### Send Message
```typescript
async function sendMessage(chatId: number, content: string) {
  const response = await fetch(`${API_BASE}/api/chats/send_message?chat_id=${chatId}`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ content })
  });
  return response.json();
}
```

### Get Chat Messages
```typescript
async function getChatMessages(chatId: number) {
  const response = await fetch(`${API_BASE}/api/chats/get_chat_messages?chat_id=${chatId}`, {
    headers: { 'Authorization': `Bearer ${TOKEN}` }
  });
  return response.json();
}
```

### Edit Chat Title
```typescript
async function editChatTitle(chatId: number, title: string) {
  const response = await fetch(`${API_BASE}/api/chats/edit_chat_title?chat_id=${chatId}&title=${encodeURIComponent(title)}`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${TOKEN}` }
  });
  return response.json();
}
```

## 📋 Common Response Formats

### AI Response
```json
{
  "content": "AI response here"
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

### Chat History
```json
{
  "messages": [
    {
      "content": "Hello",
      "type": "user"
    },
    {
      "content": "Hi there!",
      "type": "ai"
    }
  ],
  "title": "Chat Title",
  "thread_id": "abc-123-def-456"
}
```

### Success Response
```json
{
  "detail": "Operation completed successfully"
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```

## 🚨 Common Error Codes

- `400` - Bad Request (username already registered, incorrect credentials)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (chat/message doesn't exist)
- `422` - Validation Error (invalid request data)
- `500` - Internal Server Error

## 💡 Tips

1. **Always include Authorization header** for protected endpoints
2. **Use Content-Type: application/json** for POST requests with JSON data
3. **Use Content-Type: application/x-www-form-urlencoded** for login requests
4. **Handle errors gracefully** - check response status
5. **Store tokens securely** - they expire after 30 minutes
6. **Use chat IDs** from the list_chats response
7. **URL encode parameters** when using query strings

## 🔗 Full Documentation

- [Complete API Documentation](API_DOCUMENTATION.md)
- [Interactive Swagger UI](http://localhost:8000/docs)
- [ReDoc Documentation](http://localhost:8000/redoc) 