from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Web"])

templates = Jinja2Templates(directory="app/templates")


def render(request: Request, page: str, **context):

    context["request"] = request

    return templates.TemplateResponse(
        request=request,
        name=page,
        context=context
    )

# ==========================================================
# Home
# ==========================================================

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):

    return render(
        request,
        "index.html",
        title="RDO Check"
    )


# ==========================================================
# Dashboard
# ==========================================================

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):

    return render(
        request,
        "dashboard.html",
        title="Dashboard"
    )


# ==========================================================
# Processamento
# ==========================================================

@router.get("/processamento", response_class=HTMLResponse)
async def processamento(request: Request):

    return render(
        request,
        "processamento.html",
        title="Processamento"
    )


# ==========================================================
# Jobs
# ==========================================================

@router.get("/jobs", response_class=HTMLResponse)
async def jobs(request: Request):

    return render(
        request,
        "jobs.html",
        title="Jobs"
    )


# ==========================================================
# Colaboradores
# ==========================================================

@router.get("/employees", response_class=HTMLResponse)
async def employees(request: Request):

    return render(
        request,
        "employees.html",
        title="Colaboradores"
    )


# ==========================================================
# Timeline
# ==========================================================

@router.get("/timeline", response_class=HTMLResponse)
async def timeline(request: Request):

    return render(
        request,
        "timeline.html",
        title="Timeline"
    )


# ==========================================================
# Atividades
# ==========================================================

@router.get("/activities", response_class=HTMLResponse)
async def activities(request: Request):

    return render(
        request,
        "activities.html",
        title="Atividades"
    )


# ==========================================================
# Fotos
# ==========================================================

@router.get("/photos", response_class=HTMLResponse)
async def photos(request: Request):

    return render(
        request,
        "photos.html",
        title="Fotos"
    )


# ==========================================================
# Auditoria
# ==========================================================

@router.get("/audit", response_class=HTMLResponse)
async def audit(request: Request):

    return render(
        request,
        "audit.html",
        title="Auditoria"
    )


# ==========================================================
# Relatórios
# ==========================================================

@router.get("/reports", response_class=HTMLResponse)
async def reports(request: Request):

    return render(
        request,
        "reports.html",
        title="Relatórios"
    )


# ==========================================================
# Configurações
# ==========================================================

@router.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):

    return render(
        request,
        "settings.html",
        title="Configurações"
    )