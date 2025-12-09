from app import app
import os

if __name__ == "__main__":
    # Executa a aplicação Flask
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5581"))
    
    app.run(debug=debug_mode, host=host, port=port)
