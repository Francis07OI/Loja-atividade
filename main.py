from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
 
from database import get_db
from models import Categoria, Produto
 
app = FastAPI()
templates = Jinja2Templates(directory="templates")
 

# HOME

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    """Página inicial com totais de categorias e produtos."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_categorias": db.query(Categoria).count(),
        "total_produtos": db.query(Produto).count(),
    })
 
 

# CATEGORIAS

 
@app.get("/categorias", response_class=HTMLResponse)
def listar_categorias(request: Request, db: Session = Depends(get_db)):
    """Lista todas as categorias."""
    categorias = db.query(Categoria).all()
    return templates.TemplateResponse("categorias/listar.html", {
        "request": request,
        "categorias": categorias,
    })
 
 
@app.get("/categorias/nova", response_class=HTMLResponse)
def form_nova_categoria(request: Request):
    """Exibe o formulário para criar uma nova categoria."""
    return templates.TemplateResponse("categorias/form.html", {
        "request": request,
        "categoria": None,
    })
 
 
@app.post("/categorias/nova")
def criar_categoria(
    nome: str = Form(...),
    db: Session = Depends(get_db),
):
    """Cria uma nova categoria."""
    categoria = Categoria(nome=nome)
    db.add(categoria)
    db.commit()
    return RedirectResponse("/categorias", status_code=303)
 
 
@app.get("/categorias/{categoria_id}/editar", response_class=HTMLResponse)
def form_editar_categoria(
    categoria_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    """Exibe o formulário de edição de uma categoria."""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return templates.TemplateResponse("categorias/form.html", {
        "request": request,
        "categoria": categoria,
    })
 
 
@app.post("/categorias/{categoria_id}/editar")
def editar_categoria(
    categoria_id: int,
    nome: str = Form(...),
    db: Session = Depends(get_db),
):
    """Atualiza uma categoria existente."""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    categoria.nome = nome
    db.commit()
    return RedirectResponse("/categorias", status_code=303)
 
 
@app.post("/categorias/{categoria_id}/excluir")
def excluir_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
):
    """Remove uma categoria."""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(categoria)
    db.commit()
    return RedirectResponse("/categorias", status_code=303)
 