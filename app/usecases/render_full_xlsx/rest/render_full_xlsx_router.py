from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from io import BytesIO

import app.usecases.render_full_xlsx.render_full_xlsx_handler as handler

router = APIRouter()


class Params(BaseModel):
    date_from: int
    date_to: int


@router.post("/render/xlsx/")
def render_full_xlsx(params: Params):
    final_excel = handler.render_full_xlsx(date_from=params.date_from, date_to=params.date_to)
    return StreamingResponse(
        BytesIO(final_excel),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=final_report.xlsx"}
    )
