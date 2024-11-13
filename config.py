from base64 import b64decode

# Decode API ID and Hash from base64
API_ID = b64decode("MjUzMjQ1ODE=").decode()  # Your API ID
API_HASH = b64decode("MDhmZWVlNWVlYjZmYzBmMzFkNWYyZDIzYmIyYzMxZDA=").decode()  # Your API Hash

# Decode BOT Token from base64 (optional step)
BOT_TOKEN = b64decode("NzIxMTYwMzY3OkFBRlRXRm4tYldJdTd3VjAtZlV1X291MV9QZlQ1clpPZG9X").decode()  # Your Bot Token
