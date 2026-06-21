from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from core.analyzer import CodeAnalyzer
from core.cpp_analyzer import CppAnalyzer
from core.javascript_analyzer import JavaScriptAnalyzer
from core.versions import list_versions, get_version, download_asset
import os

app = FastAPI(title="Coder API")

class AnalyzeRequest(BaseModel):
    lang: str
    code: str

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    lang = req.lang.lower()
    code = req.code
    if lang == "py":
        res = CodeAnalyzer.analyze_code(code)
    elif lang == "cpp":
        res = CppAnalyzer.analyze_cpp(code)
    elif lang in ("js", "javascript"):
        res = JavaScriptAnalyzer.analyze_js(code)
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")
    return res

@app.get("/versions")
async def api_versions():
    return JSONResponse(content=list_versions())

@app.get("/versions/{version}")
async def api_version(version: str):
    v = get_version(version)
    if not v:
        raise HTTPException(status_code=404, detail="version not found")
    return JSONResponse(content=v)

@app.get("/versions/{version}/assets/{asset_name}/download")
async def api_version_asset_download(version: str, asset_name: str):
    v = get_version(version)
    if not v:
        raise HTTPException(status_code=404, detail="version not found")
    # find asset
    for a in v.get('assets', []):
        if a.get('name') == asset_name:
            asset_path = os.path.join(os.path.dirname(__file__), '..', a.get('path'))
            asset_path = os.path.abspath(asset_path)
            if not os.path.exists(asset_path):
                raise HTTPException(status_code=404, detail="asset file not found")
            return FileResponse(asset_path, filename=asset_name)
    raise HTTPException(status_code=404, detail="asset not found")
