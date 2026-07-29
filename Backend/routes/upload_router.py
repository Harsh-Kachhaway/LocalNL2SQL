from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pandas as pd
import sqlite3
import io
import os
import re
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

def sanitize_name(name: str) -> str:
    """Sanitizes text to be SQL-safe (lowercase, replace spaces/special chars with underscores)."""
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', name.strip().lower())
    return re.sub(r'_+', '_', cleaned).strip('_')

@router.post("/upload_data")
async def upload_data(
    file: UploadFile = File(...),
    table_name: Optional[str] = Form(None)  # Made optional!
):
    """
    Accepts CSV or Excel files. 
    Creates a separate SQLite table for every sheet in an Excel workbook.
    """
    try:
        contents = await file.read()
        sheets_data = {}

        if file.filename.endswith(".csv"):
            # CSVs only have 1 sheet. Use provided table_name or fallback to filename
            base_name = table_name if table_name else os.path.splitext(file.filename)[0]
            sheets_data[base_name] = pd.read_csv(io.BytesIO(contents))
            
        elif file.filename.endswith((".xls", ".xlsx")):
            # Read ALL sheets into a dict: {"Sheet1": df1, "Sheet2": df2}
            raw_sheets_data = pd.read_excel(io.BytesIO(contents), sheet_name=None)
            
            # Parse the comma-separated table names provided by the frontend
            custom_names = []
            if table_name:
                custom_names = [name.strip() for name in table_name.split(",") if name.strip()]
                
            # Map the custom names to the dataframes
            sheets_data = {}
            for i, (original_sheet_name, df) in enumerate(raw_sheets_data.items()):
                # Use custom name if available for this index, otherwise fallback to sheet name
                assigned_name = custom_names[i] if i < len(custom_names) else original_sheet_name
                sheets_data[assigned_name] = df
            
        else:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file type. Please upload a .csv, .xls, or .xlsx file."
            )

        db_path = os.getenv("DB_PATH", "sample_company.db")
        conn = sqlite3.connect(db_path)
        
        created_tables = []

        # Iterate through all sheets (or single CSV dataset)
        for raw_sheet_name, df in sheets_data.items():
            if df.empty:
                continue

            # 1. Clean table name (e.g., "Sales 2024!" -> "sales_2024")
            clean_table_name = sanitize_name(str(raw_sheet_name))
            
            # 2. Clean column names
            df.columns = [sanitize_name(str(col)) for col in df.columns]
            
            # 3. Create/Replace SQLite table
            df.to_sql(clean_table_name, conn, if_exists="replace", index=False)
            
            created_tables.append({
                "table_name": clean_table_name,
                "rows": len(df),
                "columns": list(df.columns)
            })

        conn.close()

        if not created_tables:
            raise HTTPException(status_code=400, detail="The uploaded file contains no valid data.")

        return {
            "success": True,
            "message": f"Successfully processed '{file.filename}'. Created {len(created_tables)} table(s).",
            "tables": created_tables
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")