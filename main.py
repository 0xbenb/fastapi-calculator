from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Trade P/L Calculator</h1>
    <p>Enter a completed trade to calculate its profit or loss.</p>

    <form action="/calculate" method="post">
        <input name="ticker" placeholder="Ticker (AAPL)" required>

        <select name="side">
            <option value="long">Long</option>
            <option value="short">Short</option>
        </select>

        <input name="entry_price" type="number" placeholder="Entry price" required>
        <input name="exit_price" type="number" placeholder="Exit price" required>
        <input name="quantity" type="number" placeholder="Quantity" required>

        <button>Calculate P/L</button>
    </form>
    """

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

    sign = "+" if profit_loss >= 0 else ""

    return f"""
    <h1>Trade Result</h1>
    <p>{ticker.upper()} {side.title()} trade</p>
    <p>Entry price: ${entry_price:.2f}</p>
    <p>Exit price: ${exit_price:.2f}</p>
    <p>Quantity: {quantity}</p>
    <h2>P/L: {sign}${profit_loss:.2f}</h2>
    <a href="/">Calculate another trade</a>
    """
