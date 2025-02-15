import uvicorn
from fastapi import FastAPI

from app.configuration.configuration import get_data
from app.usecases.render_full_pdf.rest import render_full_pdf_router
from app.usecases.render_full_xlsx.rest import render_full_xlsx_router

app = FastAPI()

app.include_router(router=render_full_xlsx_router.router)
app.include_router(router=render_full_pdf_router.router)

port = get_data()['server']['port']

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
