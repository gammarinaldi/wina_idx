import json
import websocket
import login
import users

res = login.call(users.list[0])
data = res.json()
access_token = data["access_token"]
refresh_token = data["refresh_token"]

def on_message(ws, message):
    # This function will be called whenever the server sends a message
    print(f"Received message: {message}")

def on_error(ws, error):
    # This function will be called if there is an error
    print(f"Error: {error}")

def on_close(ws):
    # This function will be called when the WebSocket connection is closed
    print("Connection closed")

def on_open(ws):
    # This function will be called when the WebSocket connection is opened
    print("Connection opened")
    # Send a message to the server to subscribe to the stream
    ws.send(json.dumps(
        {
            "id": 12345,
            "method": "SUBSCRIBE",
            "stream": "PRICE",
            "streamObject": "*"
        }
    ))

headers = {
    "cookie": f"access_token={access_token};refresh_token={refresh_token}"
}

# Create a WebSocket connection to the server
ws = websocket.WebSocketApp("wss://stream.ajaib.co.id:8009/ws/price",
                            header = headers,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
ws.on_open = on_open

# Run the WebSocket event loop
ws.run_forever()
