#api file
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy import inspect, text
from app.database import engine
from fastapi import APIRouter, Query
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.core.config import GOOGLE_API_KEY
import google.generativeai as genai
from app.core.auth import authenticate

router = APIRouter()
@router.get("/secure-data")
def get_secure_data(user: str = Depends(authenticate)):
    return {"message": f"Hello {user}, this is protected data!"}

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")

class QuestionRequest(BaseModel):
    question: str
    context: str

@router.post("/api/ask")
async def ask_ai(payload: QuestionRequest):
    try:
        prompt = f"""
        Context (CSV Data):
        {payload.context}

        Question:
        {payload.question}
        """
        response = model.generate_content(prompt)
        return {"answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/api/table/{table_name}")
def get_table_data(table_name: str, search: str = Query(None), limit: int = Query(None)):
    try:
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            return JSONResponse(content={"error": "Invalid table name"}, status_code=400)

        with engine.connect() as conn:
            columns = [col["name"] for col in inspector.get_columns(table_name)]

            base_query = f'SELECT * FROM "{table_name}"'
            params = {}

            if search:
                # Case-sensitive search using COLLATE BINARY
                like_clauses = [f'"{col}" LIKE :search COLLATE BINARY' for col in columns]
                where_clause = " OR ".join(like_clauses)
                base_query += f" WHERE {where_clause}"
                params["search"] = f"%{search}%"

            if limit:
                base_query += f" LIMIT {limit}"

            result = conn.execute(text(base_query), params)
            rows = [dict(row._mapping) for row in result]

        return rows

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

router = APIRouter()

@router.get("/api/tables")
def list_tables():
    inspector = inspect(engine)
    return {"tables": inspector.get_table_names()}



@router.get("/api/table/{table_name}")
async def get_table_data(
    table_name: str,
    search: str = None,
    limit: int = None
):
    try:
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            return {"error": "Invalid table name"}

        columns = [col["name"] for col in inspector.get_columns(table_name)]

        base_query = f'SELECT * FROM "{table_name}"'
        params = {}

        if search:
            # Use GLOB for case-sensitive matching
            where_clause = " OR ".join([f'"{col}" GLOB :search' for col in columns])
            base_query += f" WHERE {where_clause}"
            params["search"] = f'*{search}*'  # GLOB uses * for wildcard

        if limit:
            base_query += f" LIMIT {limit}"

        with engine.connect() as conn:
            result = conn.execute(text(base_query), params)
            rows = [dict(zip(result.keys(), row)) for row in result]

        return rows

    except Exception as e:
        return {"error": str(e)}

