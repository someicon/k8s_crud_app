import socket
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def start_page():

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            host_ip = s.getsockname()[0]
    except Exception as e:
        print(f"Error: {e}")

    return f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Server IP</title>
    </head>

    <body>
        <h1>Server IP Address</h1>
        <div id="ip-address">{host_ip}</div>
    </body>

    </html>
    """

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
