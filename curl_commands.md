# Rosy AI API - Sequential Curl Commands

## Prerequisites
- Make sure your API is running on `http://0.0.0.0:8000`
- Install `jq` for JSON formatting: `brew install jq` (macOS) or `apt-get install jq` (Ubuntu)

## Test Sequence

### 1. Health Check
```bash
curl -X GET "http://0.0.0.0:8000/health" | jq .
```

### 2a. Register a New User
```bash
curl -X POST "http://0.0.0.0:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "testpassword123"
  }' | jq .
```

### 2b. Register a New User Passwordless
```bash
curl -X POST "http://0.0.0.0:8000/api/auth/passwordless" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2"
  }' | jq .
```

### 3a. Login (if registration fails due to existing user)
```bash
curl -X POST "http://0.0.0.0:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpassword123" | jq .
```

### 3b. Login (if registration fails due to existing user) without password
```bash
curl -X POST "http://0.0.0.0:8000/api/auth/passwordless" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2"
  }' | jq .
```

### 4. Create a New Chat
```bash
curl -X POST "http://0.0.0.0:8000/api/chats/create_chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Test Chat"
  }' | jq .
```

### 5. List All Chats
```bash
curl -X GET "http://0.0.0.0:8000/api/chats/list_chats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### 6. Send First Message (Auto-sets title)
```bash
curl -X POST "http://0.0.0.0:8000/api/chats/send_message?chat_id=CHAT_ID"" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "Hello! This is my first message to test the AI."
  }' | jq .
```

### 7. Get Chat Messages
```bash
curl -X GET "http://0.0.0.0:8000/api/chats/get_chat_messages?chat_id=CHAT_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### 8. Send Second Message
```bash
curl -X POST "http://0.0.0.0:8000/api/chats/send_message?chat_id=CHAT_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "Can you tell me about artificial intelligence?"
  }' | jq .
```

### 9. Get Updated Messages
```bash
curl -X GET "http://0.0.0.0:8000/api/chats/get_chat_messages?chat_id=CHAT_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### 10. Edit Chat Title
```bash
curl -X PUT "http://0.0.0.0:8000/api/chats/edit_chat_title?title=Updated%20Test%20Chat&chat_id=CHAT_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### 11. List Chats Again (see updated title)
```bash
curl -X GET "http://0.0.0.0:8000/api/chats/list_chats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### 12. Create Second Chat
```bash
curl -X POST "http://0.0.0.0:8000/api/chats/create_chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Second Test Chat"
  }' | jq .
```

### 13. Send Message to Second Chat
```bash
curl -X POST "http://0.0.0.0:8000/api/chats/send_message?chat_id=CHAT_ID"" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "This is a message in the second chat thread."
  }' | jq .
```

### 14. Test Unauthorized Access (should fail)
```bash
curl -X GET "http://0.0.0.0:8000/api/chats/list_chats" | jq .
```

### 15. Test Invalid Chat ID (should fail)
```bash
curl -X GET "http://0.0.0.0:8000/api/chats/get_chat_messages?chat_id=99999" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### 16. Test Passwordless Auth
```bash
curl -X POST "http://0.0.0.0:8000/api/auth/passwordless" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "passwordless_user"
  }' | jq .
```

### 17. Final Chat List
```bash
curl -X GET "http://0.0.0.0:8000/api/chats/list_chats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### 18. Delete Chat (Cleanup)
```bash
curl -X DELETE "http://0.0.0.0:8000/api/chats/delete_chat?chat_id=CHAT_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

## Quick Test Script

You can also run the automated test script:

```bash
chmod +x test_api.sh
./test_api.sh
```

## Notes

- Replace `YOUR_ACCESS_TOKEN` with the actual token from step 2 or 3
- Replace `CHAT_ID` with the actual chat ID from step 4
- Replace `CHAT_ID_2` with the actual second chat ID from step 12
- The API uses LangGraph checkpointer for conversation persistence
- Messages are stored in LangGraph threads, not in a separate Message table
- Chat titles are automatically set from the first message content 