from fastapi import APIRouter

from app.usecases.render_full_pdf.render_full_pdf_handler import render_full_pdf as render_full

router = APIRouter()


@router.post("/render/pdf/")
async def render_full_pdf(date_from: int, date_to: int):
    return await render_full(date_from=date_from, date_to=date_to)