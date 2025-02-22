from fastapi import APIRouter
from fastapi.openapi.models import Response
from pydantic import BaseModel
import app.usecases.render_full_xlsx.render_full_xlsx_handler as handler


# from app.usecases.render_full_xlsx.render_full_xlsx_handler import merge_xlsx as render_full

router = APIRouter()

class Params(BaseModel):
    date_from: int
    date_to: int


@router.post("/render/xlsx/")
def render_full_xlsx(params: Params):
    # return render_full(date_from=params.date_from, date_to=params.date_to)
    # excel_bytes = pyo3_rust.render_excel(params.date_from, params.date_to)

    handler.render_full_xlsx()
    return None
    # return Response(
    #     content="done",
    #     description="description",
    #     headers={"Content-Disposition": "attachment; filename=final_report.xlsx"}
    # )