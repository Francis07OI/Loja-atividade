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
 
 

cria