

class WebSocketConfig:
    """Configuration settings for WebSocket server"""
    
    HOST = "0.0.0.0"
    PORT = 8000
    

    MAX_ROUNDS = 3
    MESSAGE_DELAY_SECONDS = 0.5 
    # CORS settings
    ALLOWED_ORIGINS = ["http://localhost:3000"]  # Next.js default port
    
    # LLM settings
    DEFAULT_TEMPERATURE = 0.7
    MAX_TOKENS_PER_RESPONSE = 500