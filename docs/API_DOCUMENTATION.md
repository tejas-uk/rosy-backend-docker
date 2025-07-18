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

### User Registration

**Endpoint:** `POST /api/auth/register`

Register a new user with username, password, and optional email.

#### cURL Example
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password",
    "email": "john@example.com"
  }'
```

#### TypeScript Example
```typescript
interface UserCreate {
  username: string;
  password: string;
  email?: string;
}

async function registerUser(userData: UserCreate): Promise<AuthResponse> {
  const response = await fetch('http://localhost:8000/api/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    throw new Error(`Registration failed: ${response.statusText}`);
  }

  return response.json();
}
```

### User Login

**Endpoint:** `POST /api/auth/login`

Login with username and password using OAuth2 form data.

#### cURL Example
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=secure_password"
```

#### TypeScript Example
```typescript
async function loginUser(username: string, password: string): Promise<AuthResponse> {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Login failed: ${response.statusText}`);
  }

  return response.json();
}
```

### Get Current User

**Endpoint:** `GET /api/auth/me`

Get the current authenticated user's information.

#### cURL Example
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### TypeScript Example
```typescript
interface User {
  id: number;
  username: string;
  email?: string;
  auth_provider: string;
  created_at: string;
  last_login_at?: string;
}

async function getCurrentUser(token: string): Promise<User> {
  const response = await fetch('http://localhost:8000/api/auth/me', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get user: ${response.statusText}`);
  }

  return response.json();
}
```

### Logout

**Endpoint:** `POST /api/auth/logout`

Logout the current user.

#### cURL Example
```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Response
```json
{
  "detail": "Logged out successfully"
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

### Get Chat Messages

**Endpoint:** `GET /api/chats/get_chat_messages`

Retrieve the conversation history for a specific chat.

#### cURL Example
```bash
curl -X GET "http://localhost:8000/api/chats/get_chat_messages?chat_id=1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### TypeScript Example
```typescript
interface SimpleMessage {
  content: string;
  type: string; // "user" or "ai"
}

interface ChatHistory {
  messages: SimpleMessage[];
  title: string;
  thread_id: string;
}

async function getChatMessages(token: string, chatId: number): Promise<ChatHistory> {
  const response = await fetch(`http://localhost:8000/api/chats/get_chat_messages?chat_id=${chatId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get chat messages: ${response.statusText}`);
  }

  return response.json();
}

// Usage
const messages = await getChatMessages(auth.access_token, 1);
console.log('Chat messages:', messages);
```

#### Response
```json
{
  "messages": [
    {
      "content": "Hello, how are you?",
      "type": "user"
    },
    {
      "content": "Hello! I'm doing well, thank you for asking. How can I help you today?",
      "type": "ai"
    }
  ],
  "title": "My First Chat",
  "thread_id": "abc-123-def-456"
}
```

### Send Message

**Endpoint:** `POST /api/chats/send_message`

Send a message to the AI assistant in a specific chat.

#### cURL Example
```bash
curl -X POST "http://localhost:8000/api/chats/send_message?chat_id=1" \
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

interface AIResponse {
  content: string;
}

async function sendMessage(
  token: string, 
  chatId: number, 
  content: string
): Promise<AIResponse> {
  const response = await fetch(`http://localhost:8000/api/chats/send_message?chat_id=${chatId}`, {
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
  "content": "I don't have access to real-time weather information, but I can help you find weather data or answer other questions. Would you like me to help you search for weather information?"
}
```

### Edit Chat Title

**Endpoint:** `PUT /api/chats/edit_chat_title`

Update the title of a specific chat.

#### cURL Example
```bash
curl -X PUT "http://localhost:8000/api/chats/edit_chat_title?chat_id=1&title=Updated%20Chat%20Title" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### TypeScript Example
```typescript
async function editChatTitle(token: string, chatId: number, title: string): Promise<void> {
  const response = await fetch(`http://localhost:8000/api/chats/edit_chat_title?chat_id=${chatId}&title=${encodeURIComponent(title)}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to edit chat title: ${response.statusText}`);
  }
}
```

#### Response
```json
{
  "detail": "Chat title updated successfully"
}
```

### Delete Chat

**Endpoint:** `DELETE /api/chats/{chat_id}/delete_chat`

Delete a specific chat and all its messages.

#### cURL Example
```bash
curl -X DELETE "http://localhost:8000/api/chats/1/delete_chat" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### TypeScript Example
```typescript
interface DeleteResponse {
  detail: string;
}

async function deleteChat(token: string, chatId: number): Promise<DeleteResponse> {
  const response = await fetch(`http://localhost:8000/api/chats/${chatId}/delete_chat`, {
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
console.log('Delete result:', result.detail);
```

#### Response
```json
{
  "detail": "Chat deleted successfully"
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
  "status": "healthy"
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
  "status": "healthy"
}
```

## ❌ Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Username already registered"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

#### 403 Forbidden
```json
{
  "detail": "Not authorized to access this chat"
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
  "detail": "Failed to update chat title"
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

  async register(userData: UserCreate): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    
    this.setToken(response.access_token);
    return response;
  }

  async login(username: string, password: string): Promise<AuthResponse> {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await this.request<AuthResponse>('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });
    
    this.setToken(response.access_token);
    return response;
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/api/auth/me');
  }

  async logout(): Promise<void> {
    await this.request('/api/auth/logout', { method: 'POST' });
    this.token = null;
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

  async getChatMessages(chatId: number): Promise<ChatHistory> {
    return this.request<ChatHistory>(`/api/chats/get_chat_messages?chat_id=${chatId}`);
  }

  async sendMessage(chatId: number, content: string): Promise<AIResponse> {
    return this.request<AIResponse>(`/api/chats/send_message?chat_id=${chatId}`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    });
  }

  async editChatTitle(chatId: number, title: string): Promise<void> {
    await this.request(`/api/chats/edit_chat_title?chat_id=${chatId}&title=${encodeURIComponent(title)}`, {
      method: 'PUT',
    });
  }

  async deleteChat(chatId: number): Promise<DeleteResponse> {
    return this.request<DeleteResponse>(`/api/chats/${chatId}/delete_chat`, {
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

    // Get chat messages
    const messages = await client.getChatMessages(chat.id);
    console.log('Chat messages:', messages.messages.length);

    // Edit chat title
    await client.editChatTitle(chat.id, 'Updated Chat Title');

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