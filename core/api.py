from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.analyzer import CodeAnalyzer
from core.cpp_analyzer import CppAnalyzer
from core.javascript_analyzer import JavaScriptAnalyzer

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
