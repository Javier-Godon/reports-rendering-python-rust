from fastapi import APIRouter
from pydantic import BaseModel

from app.usecases.render_full_xlsx.render_full_xlsx_handler import render_full_xlsx as render_full

router = APIRouter()

class Params(BaseModel):
    date_from: int
    date_to: int


@router.post("/render/xlsx/")
async def render_full_xlsx(params: Params):
    return await render_full(date_from=params.date_from, date_to=params.date_to)