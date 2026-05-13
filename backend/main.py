import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pricing_core import load_market_data, predict_price_etb, train_pipeline


class PredictRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=500)


class PredictResponse(BaseModel):
    product_name: str
    price_etb: float


_model = None
_row_count: int = 0


def _csv_path() -> Path:
    env = os.environ.get("MARKET_DATA_PATH")
    if env:
        return Path(env).expanduser().resolve()
    return ROOT / "market_data.csv"


def _load_model():
    global _model, _row_count
    path = _csv_path()
    if not path.is_file():
        raise FileNotFoundError(f"market data not found: {path}")
    df = load_market_data(path)
    _model = train_pipeline(df)
    _row_count = len(df)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _load_model()
    yield


app = FastAPI(title="Dynamic pricing API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "training_rows": _row_count}


@app.post("/predict", response_model=PredictResponse)
def predict(body: PredictRequest):
    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    price = predict_price_etb(_model, body.product_name.strip())
    return PredictResponse(product_name=body.product_name.strip(), price_etb=round(price, 2))
