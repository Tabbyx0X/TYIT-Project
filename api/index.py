from app import app

# Export the Flask app as the Vercel handler
# Vercel's Python runtime will automatically call this
app = app
