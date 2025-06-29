#upload file
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from app.database import engine
import io
from app.core.auth import authenticate

from fastapi import Depends 

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.get("/")
async def protected_ui_page(request: Request, _=Depends(authenticate)):
    return await upload_get(request)

async def upload_get(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request, "table": None, "summary": {}})

@router.get("/query", response_class=HTMLResponse)
async def query_page(request: Request):
    return templates.TemplateResponse("query.html", {"request": request})


@router.get("/", response_class=HTMLResponse)




@router.post("/", response_class=HTMLResponse)
@router.post("/", response_class=HTMLResponse)
async def upload_post(request: Request, csv_file: UploadFile = File(...)):
    summary = {}
    table_html = None

    if csv_file.filename.endswith(".csv"):
        file_path = os.path.join(UPLOAD_FOLDER, csv_file.filename)

        with open(file_path, "wb") as f:
            f.write(await csv_file.read())

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            return templates.TemplateResponse("upload.html", {
                "request": request,
                "table": None,
                "summary": {},
                "message": f"Failed to read CSV: {str(e)}"
            })

        table_name = os.path.splitext(csv_file.filename)[0].replace(" ", "_")
        try:
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            message = f"Stored in DB table: {table_name}"
        except Exception as e:
            message = f"DB error: {str(e)}"

        table_html = df.to_html(classes="table table-bordered text-center table-striped", index=False)
        summary["num_rows"] = df.shape[0]
        summary["num_cols"] = df.shape[1]
        summary["columns"] = list(df.columns)
        summary["dtypes"] = df.dtypes.apply(str).to_dict()
        summary["missing"] = df.isnull().sum().to_dict()

        return templates.TemplateResponse("upload.html", {
            "request": request,
            "table": table_html,
            "summary": summary,
            "message": message
        })

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "table": None,
        "summary": {},
        "message": "Please upload a valid CSV file"
    })
@router.post("/api/upload")
async def upload_csv(csv_file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, csv_file.filename)
    with open(file_path, "wb") as f:
        f.write(await csv_file.read())

    try:
        df = pd.read_csv(file_path)
        table_name = os.path.splitext(csv_file.filename)[0].replace(" ", "_")
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        return {"message": f"Uploaded to table '{table_name}'"}
    except Exception as e:
        return {"error": str(e)}