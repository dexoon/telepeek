# TelePeek

A FastAPI-based REST API that provides user information from Telegram usernames.

## Features

- 🔍 **User Lookup**: Get detailed information about Telegram users by username
- 🚀 **FastAPI**: Modern, fast web framework with automatic API documentation
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 🔒 **Security**: Non-root container execution and proper error handling

## API Endpoints

### Get User Information
```
GET /{username}
```

**Parameters:**
- `username` (path): Telegram username (without @)

**Response:**
```json
{
  "id": 123456789,
  "username": "example_user",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "is_bot": false,
  "verified": true,
  "restricted": false,
  "scam": false,
  "language_code": "en"
}
```

**Status Codes:**
- `200`: User found successfully
- `404`: User not found
- `400`: Invalid username format
- `500`: Internal server error

## Prerequisites

- Python 3.12+
- Telegram Bot Token
- Telegram API ID and API Hash

## Setup

### 1. Get Telegram API Credentials

1. Visit [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Note down your `API_ID` and `API_HASH`
6. Create a bot with [@BotFather](https://t.me/botfather) and get your `BOT_TOKEN`

### 2. Environment Variables

Create a `.env` file in the project root:

```bash
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
PORT=80  # Optional, defaults to 80
```

### 3. Installation

#### Using uv (Recommended)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the application
uv run python main.py
```

#### Using pip
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### 4. Docker Deployment

```bash
# Build the image
docker build -t telepeek .

# Run the container
docker run -p 80:80 \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  -e BOT_TOKEN=your_bot_token \
  telepeek
```

## Usage Examples

### Using curl
```bash
# Get user information
curl http://localhost:80/user/username

# Example response
curl http://localhost:80/user/elonmusk
```

### Using Python requests
```python
import requests

response = requests.get('http://localhost:80/user/username')
if response.status_code == 200:
    user_data = response.json()
    print(f"User: {user_data['first_name']} {user_data['last_name']}")
    print(f"Username: @{user_data['username']}")
    print(f"Verified: {user_data['verified']}")
```

### Using JavaScript fetch
```javascript
fetch('http://localhost:80/user/username')
  .then(response => response.json())
  .then(data => {
    console.log('User:', data.first_name, data.last_name);
    console.log('Username:', '@' + data.username);
    console.log('Verified:', data.verified);
  })
  .catch(error => console.error('Error:', error));
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- **Swagger UI**: http://localhost:80/docs
- **ReDoc**: http://localhost:80/redoc



## Error Handling

The API provides comprehensive error handling:

- **404 Not Found**: Username doesn't exist or user is not accessible
- **400 Bad Request**: Invalid username format
- **500 Internal Server Error**: Server-side errors (logged for debugging)

## Development

### Project Structure
```
telepeek/
├── main.py              # FastAPI application
├── pyproject.toml       # Project dependencies
├── uv.lock             # Locked dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── .dockerignore       # Docker ignore rules
└── README.md           # This file
```

### Running in Development Mode
```bash
# Install development dependencies
uv sync --dev

# Run with auto-reload
uv run python main.py
```

## Security Considerations

- The application runs as a non-root user in Docker
- Environment variables are used for sensitive configuration
- Input validation is performed on usernames
- Error messages don't expose internal system details

## Rate Limiting

Be aware of Telegram's API rate limits:
- **Flood Wait**: 429 errors when rate limit is exceeded
- **User Privacy**: Some users may have privacy settings that prevent data access
- **Bot Limitations**: Bots have different access levels than user accounts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues:

1. Check the API documentation at `/docs`
2. Verify your Telegram API credentials
3. Check the application logs for error details

## Disclaimer

This tool is for educational and legitimate use only. Please respect Telegram's Terms of Service and user privacy. The developers are not responsible for misuse of this application.
