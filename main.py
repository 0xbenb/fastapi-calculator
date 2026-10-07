from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

def page(content):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trade P/L Calculator</title>
        <style>
            body {{ font-family: Arial; background: #f4f6f8; margin: 0; }}
            main {{ max-width: 600px; margin: 70px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px #ccc; }}
            input, select, button {{ padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }}
            button {{ background: #2563eb; color: white; border: 0; border-radius: 5px; cursor: pointer; }}
            .result {{ background: #f4f6f8; padding: 15px; border-radius: 6px; }}
            a {{ color: #2563eb; }}
        </style>
    </head>
    <body><main>{content}</main></body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
def home():
    return page("""
        <h1>Trade P/L Calculator</h1>
        <p>Enter a completed trade to calculate its profit or loss.</p>

        <form action="/calculate" method="post">
            <input name="ticker" placeholder="Ticker (AAPL)" required>

            <select name="side">
                <option value="long">Long</option>
                <option value="short">Short</option>
            </select>

            <input name="entry_price" type="number" step="0.01" placeholder="Entry price" required>
            <input name="exit_price" type="number" step="0.01" placeholder="Exit price" required>
            <input name="quantity" type="number" placeholder="Quantity" required>

            <button>Calculate P/L</button>
        </form>
    """)

@app.post("/calculate", response_class=HTMLResponse)
def calculate(
    ticker: str = Form(...),
    side: str = Form(...),
    entry_price: float = Form(...),
    exit_price: float = Form(...),
    quantity: int = Form(...),
):
    profit_loss = (exit_price - entry_price) * quantity

    if side == "short":
        profit_loss *= -1

    color = "#15803d" if profit_loss >= 0 else "#dc2626"
    sign = "+" if profit_loss >= 0 else ""

    return page(f"""
        <h1>Trade Result</h1>

        <div class="result">
            <p><b>{ticker.upper()} · {side.title()}</b></p>
            <p>Entry price: ${entry_price:.2f}</p>
            <p>Exit price: ${exit_price:.2f}</p>
            <p>Quantity: {quantity}</p>
            <h2 style="color: {color}">P/L: {sign}${profit_loss:.2f}</h2>
        </div>

        <p><a href="/">← Calculate another trade</a></p>
    """)
