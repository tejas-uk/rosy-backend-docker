# Rosy AI API Documentation

Complete API reference with curl commands and TypeScript examples for the Rosy AI chat backend.

## 📋 Table of Contents

- [Authentication](#authentication)
- [Chat Management](#chat-management)
- [Health & Status](#health--status)
- [Error Handling](#error-handling)
- [TypeScript Client](#typescript-client)

## 🔐 Authentication

### Passwordless Authentication

**Endpoint:** `POST /api/auth/passwordless`

Authenticate a user with a username (passwordless authentication).

#### cURL Example
```bash
curl -X POST "http://localhost:8000/api/auth/passwordless" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe"
  }'
```

#### TypeScript Example
```typescript
interface PasswordlessAuthRequest {
  username: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
}

async function authenticateUser(username: string): Promise<AuthResponse> {
  const response = await fetch('http://localhost:8000/api/auth/passwordless', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username }),
  });

  if (!response.ok) {
    throw new Error(`Authentication failed: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const auth = await authenticateUser('john_doe');
console.log('Access token:', auth.access_token);
```

#### Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Verify Authentication Token

**Endpoint:** `POST /api/auth/verify`

Verify the validity of an authentication token.

#### cURL Example
```bash
curl -X POST "http://localhost:8000/api/auth/verify" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{}'
```

#### TypeScript Example
```typescript
interface VerifyResponse {
  valid: boolean;
  user_id: string;
  username: string;
}

async function verifyToken(token: string): Promise<VerifyResponse> {
  const response = await fetch('http://localhost:8000/api/auth/verify', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({}),
  });

  if (!response.ok) {
    throw new Error(`Token verification failed: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const verification = await verifyToken(auth.access_token);
console.log('Token valid:', verification.valid);
```

#### Response
```json
{
  "valid": true,
  "user_id": "123",
  "username": "john_doe"
}
```

## 💬 Chat Management

### List User Chats

**Endpoint:** `GET /api/chats/list_chats`

Retrieve all chats for the authenticated user.

#### cURL Example
```bash
curl -X GET "http://localhost:8000/api/chats/list_chats" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### TypeScript Example
```typescript
interface Chat {
  id: number;
  user_id: number;
  title: string;
  thread_id: string;
  created_at: string;
  updated_at: string;
  is_deleted: boolean;
}

async function listChats(token: string): Promise<Chat[]> {
  const response = await fetch('http://localhost:8000/api/chats/list_chats', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to list chats: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const chats = await listChats(auth.access_token);
console.log('User chats:', chats);
```

#### Response
```json
[
  {
    "id": 1,
    "user_id": 123,
    "title": "My First Chat",
    "thread_id": "abc-123-def-456",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z",
    "is_deleted": false
  }
]
```

### Create New Chat

**Endpoint:** `POST /api/chats/create_chat`

Create a new chat session for the authenticated user.

#### cURL Example
```bash
curl -X POST "http://localhost:8000/api/chats/create_chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "New Chat Session"
  }'
```

#### TypeScript Example
```typescript
interface CreateChatRequest {
  title: string;
}

async function createChat(token: string, title: string): Promise<Chat> {
  const response = await fetch('http://localhost:8000/api/chats/create_chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    throw new Error(`Failed to create chat: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const newChat = await createChat(auth.access_token, 'New Chat Session');
console.log('Created chat:', newChat);
```

#### Response
```json
{
  "id": 2,
  "user_id": 123,
  "title": "New Chat Session",
  "thread_id": "xyz-789-abc-123",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z",
  "is_deleted": false
}
```

### Get Chat History

**Endpoint:** `GET /api/chats/{chat_id}/history`

Retrieve the conversation history for a specific chat.

#### cURL Example
```bash
curl -X GET "http://localhost:8000/api/chats/1/history" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### TypeScript Example
```typescript
interface Message {
  id: number;
  chat_id: number;
  content: string;
  role: 'user' | 'assistant';
  created_at: string;
}

interface ChatHistory {
  chat: Chat;
  messages: Message[];
}

async function getChatHistory(token: string, chatId: number): Promise<ChatHistory> {
  const response = await fetch(`http://localhost:8000/api/chats/${chatId}/history`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get chat history: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const history = await getChatHistory(auth.access_token, 1);
console.log('Chat history:', history);
```

#### Response
```json
{
  "chat": {
    "id": 1,
    "user_id": 123,
    "title": "My First Chat",
    "thread_id": "abc-123-def-456",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z",
    "is_deleted": false
  },
  "messages": [
    {
      "id": 1,
      "chat_id": 1,
      "content": "Hello, how are you?",
      "role": "user",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "chat_id": 1,
      "content": "Hello! I'm doing well, thank you for asking. How can I help you today?",
      "role": "assistant",
      "created_at": "2024-01-15T10:30:05Z"
    }
  ]
}
```

### Send Message

**Endpoint:** `POST /api/chats/{chat_id}/send_message`

Send a message to the AI assistant in a specific chat.

#### cURL Example
```bash
curl -X POST "http://localhost:8000/api/chats/1/send_message" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "content": "What is the weather like today?"
  }'
```

#### TypeScript Example
```typescript
interface SendMessageRequest {
  content: string;
}

interface SendMessageResponse {
  content: string;
  message_id: number;
  timestamp: string;
}

async function sendMessage(
  token: string, 
  chatId: number, 
  content: string
): Promise<SendMessageResponse> {
  const response = await fetch(`http://localhost:8000/api/chats/${chatId}/send_message`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ content }),
  });

  if (!response.ok) {
    throw new Error(`Failed to send message: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const response = await sendMessage(auth.access_token, 1, 'What is the weather like today?');
console.log('AI response:', response.content);
```

#### Response
```json
{
  "content": "I don't have access to real-time weather information, but I can help you find weather data or answer other questions. Would you like me to help you search for weather information?",
  "message_id": 3,
  "timestamp": "2024-01-15T11:05:00Z"
}
```

### Delete Chat

**Endpoint:** `DELETE /api/chats/{chat_id}`

Delete a specific chat and all its messages.

#### cURL Example
```bash
curl -X DELETE "http://localhost:8000/api/chats/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### TypeScript Example
```typescript
interface DeleteResponse {
  success: boolean;
  message: string;
}

async function deleteChat(token: string, chatId: number): Promise<DeleteResponse> {
  const response = await fetch(`http://localhost:8000/api/chats/${chatId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to delete chat: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const result = await deleteChat(auth.access_token, 1);
console.log('Delete result:', result.message);
```

#### Response
```json
{
  "success": true,
  "message": "Chat deleted successfully"
}
```

## 🏥 Health & Status

### Application Health Check

**Endpoint:** `GET /health`

Check the overall health of the application.

#### cURL Example
```bash
curl -X GET "http://localhost:8000/health"
```

#### TypeScript Example
```typescript
interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}

async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch('http://localhost:8000/health');

  if (!response.ok) {
    throw new Error(`Health check failed: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const health = await checkHealth();
console.log('App status:', health.status);
```

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T11:00:00Z",
  "version": "1.0.0"
}
```

### Chat Service Health Check

**Endpoint:** `GET /api/chats/health`

Check the health of the chat service specifically.

#### cURL Example
```bash
curl -X GET "http://localhost:8000/api/chats/health"
```

#### TypeScript Example
```typescript
interface ChatHealthResponse {
  status: string;
  checkpointer: string;
  memory_service: string;
  ai_agents: string;
}

async function checkChatHealth(): Promise<ChatHealthResponse> {
  const response = await fetch('http://localhost:8000/api/chats/health');

  if (!response.ok) {
    throw new Error(`Chat health check failed: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const chatHealth = await checkChatHealth();
console.log('Chat service status:', chatHealth.status);
```

#### Response
```json
{
  "status": "healthy",
  "checkpointer": "connected",
  "memory_service": "connected",
  "ai_agents": "ready"
}
```

## ❌ Error Handling

### Common Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

#### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

#### 404 Not Found
```json
{
  "detail": "Chat not found"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "content"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

### Error Handling in TypeScript

```typescript
class RosyAIError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: any
  ) {
    super(message);
    this.name = 'RosyAIError';
  }
}

async function handleApiRequest<T>(
  request: () => Promise<Response>
): Promise<T> {
  try {
    const response = await request();
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new RosyAIError(
        errorData.detail || `HTTP ${response.status}`,
        response.status,
        errorData
      );
    }
    
    return response.json();
  } catch (error) {
    if (error instanceof RosyAIError) {
      throw error;
    }
    throw new RosyAIError(
      'Network error',
      0,
      { originalError: error }
    );
  }
}

// Usage
try {
  const chats = await handleApiRequest(() =>
    fetch('http://localhost:8000/api/chats/list_chats', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
  );
  console.log('Chats:', chats);
} catch (error) {
  if (error instanceof RosyAIError) {
    console.error(`API Error ${error.status}:`, error.message);
  } else {
    console.error('Unexpected error:', error);
  }
}
```

## 🔧 TypeScript Client

### Complete TypeScript Client Class

```typescript
class RosyAIClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  setToken(token: string) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new RosyAIError(
        errorData.detail || `HTTP ${response.status}`,
        response.status,
        errorData
      );
    }

    return response.json();
  }

  // Authentication
  async authenticate(username: string): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/auth/passwordless', {
      method: 'POST',
      body: JSON.stringify({ username }),
    });
    
    this.setToken(response.access_token);
    return response;
  }

  async verifyToken(): Promise<VerifyResponse> {
    return this.request<VerifyResponse>('/api/auth/verify', {
      method: 'POST',
      body: JSON.stringify({}),
    });
  }

  // Chat Management
  async listChats(): Promise<Chat[]> {
    return this.request<Chat[]>('/api/chats/list_chats');
  }

  async createChat(title: string): Promise<Chat> {
    return this.request<Chat>('/api/chats/create_chat', {
      method: 'POST',
      body: JSON.stringify({ title }),
    });
  }

  async getChatHistory(chatId: number): Promise<ChatHistory> {
    return this.request<ChatHistory>(`/api/chats/${chatId}/history`);
  }

  async sendMessage(chatId: number, content: string): Promise<SendMessageResponse> {
    return this.request<SendMessageResponse>(`/api/chats/${chatId}/send_message`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    });
  }

  async deleteChat(chatId: number): Promise<DeleteResponse> {
    return this.request<DeleteResponse>(`/api/chats/${chatId}`, {
      method: 'DELETE',
    });
  }

  // Health Checks
  async checkHealth(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }

  async checkChatHealth(): Promise<ChatHealthResponse> {
    return this.request<ChatHealthResponse>('/api/chats/health');
  }
}

// Usage Example
async function main() {
  const client = new RosyAIClient('http://localhost:8000');

  try {
    // Authenticate
    const auth = await client.authenticate('john_doe');
    console.log('Authenticated:', auth.access_token);

    // Check health
    const health = await client.checkHealth();
    console.log('App health:', health.status);

    // Create a new chat
    const chat = await client.createChat('My New Chat');
    console.log('Created chat:', chat.title);

    // Send a message
    const response = await client.sendMessage(chat.id, 'Hello, AI!');
    console.log('AI response:', response.content);

    // Get chat history
    const history = await client.getChatHistory(chat.id);
    console.log('Chat messages:', history.messages.length);

  } catch (error) {
    if (error instanceof RosyAIError) {
      console.error(`API Error ${error.status}:`, error.message);
    } else {
      console.error('Unexpected error:', error);
    }
  }
}

// Run the example
main();
```

## 📝 Notes

- All timestamps are in ISO 8601 format (UTC)
- Authentication tokens expire after 30 minutes by default
- Rate limiting may apply to prevent abuse
- WebSocket support for real-time chat is planned for future releases
- All responses are JSON format
- Error responses include detailed information for debugging

## 🔗 Additional Resources

- [Interactive API Documentation](http://localhost:8000/docs)
- [ReDoc Documentation](http://localhost:8000/redoc)
- [GitHub Repository](https://github.com/your-org/rosy-ai-backend)
- [Support & Issues](https://github.com/your-org/rosy-ai-backend/issues) 