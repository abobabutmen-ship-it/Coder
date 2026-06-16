import os
import sys
import json
import click
from core.analyzer import CodeAnalyzer
from core.fixer import CodeFixer
from core.generator import CodeGenerator
from core.logging_handler import log_analysis, log_fix, log_improvements
from core.cpp_analyzer import CppAnalyzer
from core.javascript_analyzer import JavaScriptAnalyzer
from core.llm_client import LLMClient, LLMAvailable

@click.group()
def cli():
    """Coder CLI — analyze / fix / improve code"""
    pass

def _read_code(file, code):
    if file:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    if code:
        return code
    click.echo("No code provided (use --file or --code).", err=True)
    sys.exit(2)

@cli.command()
@click.option("--lang", type=click.Choice(["py","js","cpp"]), required=True)
@click.option("--file", "-f", type=click.Path(exists=True), help="Path to file")
@click.option("--code", "-c", help="Raw code string")
def analyze(lang, file, code):
    """Analyze code for issues"""
    src = _read_code(file, code)
    if lang == "py":
        res = CodeAnalyzer.analyze_code(src)
    elif lang == "cpp":
        res = CppAnalyzer.analyze_cpp(src)
    else:
        res = JavaScriptAnalyzer.analyze_js(src)
    click.echo(json.dumps(res, ensure_ascii=False, indent=2))
    log_analysis(res)

@cli.command()
@click.option("--file", "-f", type=click.Path(exists=True), help="Path to file")
@click.option("--code", "-c", help="Raw code string")
@click.option("--out", "-o", type=click.Path(), help="Write fixed code to file")
def fix(file, code, out):
    """Attempt to fix Python code (heuristic)"""
    src = _read_code(file, code)
    # analyze first
    res = CodeAnalyzer.analyze_code(src)
    if res.get("success"):
        click.echo("No issues found.")
        return
    fix_res = CodeFixer.fix_code(src, res)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(fix_res["fixed_code"])
        click.echo(f"Wrote fixed code to {out}")
    else:
        click.echo(fix_res["fixed_code"])
    log_fix(fix_res["fixed_code"])

@cli.command()
@click.option("--file", "-f", type=click.Path(exists=True), help="Path to file")
@click.option("--code", "-c", help="Raw code string")
@click.option("--use-llm", is_flag=True, help="Use remote LLM if configured")
@click.option("--out", "-o", type=click.Path(), help="Write improved code to file")
def improve(file, code, use_llm, out):
    """Improve code: local generator or optional LLM"""
    src = _read_code(file, code)
    if use_llm and LLMAvailable():
        client = LLMClient()
        improved = client.improve_code(src)
        improved_code = improved.get("improved_code") or improved.get("result") or src
        notes = improved.get("notes", [])
    else:
        improved = CodeGenerator.improve_code(src)
        improved_code = improved["improved_code"]
        notes = improved["notes"]
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(improved_code)
        click.echo(f"Wrote improved code to {out}")
    else:
        click.echo(improved_code)
    log_improvements(improved_code)
    if notes:
        click.echo("Notes: " + ", ".join(notes), err=False)

@cli.command()
@click.option("--file", "-f", type=click.Path(exists=True), help="Path to file")
@click.option("--code", "-c", help="Raw code string")
@click.option("--use-llm", is_flag=True, help="Use LLM if configured")
@click.option("--out-dir", "-o", type=click.Path(), help="Directory to write outputs")
def run_all(file, code, use_llm, out_dir):
    """Run analyze -> fix -> improve pipeline"""
    src = _read_code(file, code)
    res = CodeAnalyzer.analyze_code(src)
    click.echo("ANALYSIS:")
    click.echo(json.dumps(res, ensure_ascii=False, indent=2))
    log_analysis(res)

    fixed = src
    if not res.get("success"):
        fix_res = CodeFixer.fix_code(src, res)
        fixed = fix_res["fixed_code"]
        click.echo("FIX:")
        click.echo(json.dumps(fix_res, ensure_ascii=False, indent=2))
        log_fix(fixed)

    if use_llm and LLMAvailable():
        client = LLMClient()
        improved = client.improve_code(fixed)
        improved_code = improved.get("improved_code") or improved.get("result") or fixed
    else:
        improved = CodeGenerator.improve_code(fixed)
        improved_code = improved["improved_code"]

    click.echo("IMPROVED:")
    click.echo(improved_code)
    log_improvements(improved_code)

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        open(os.path.join(out_dir, "fixed.py"), "w", encoding="utf-8").write(fixed)
        open(os.path.join(out_dir, "improved.py"), "w", encoding="utf-8").write(improved_code)
        click.echo(f"Wrote results to {out_dir}")
