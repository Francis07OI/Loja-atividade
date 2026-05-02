@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    """Página inicial com totais de categorias e produtos."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_categorias": db.query(Categoria).count(),
        "total_produtos": db.query(Produto).count(),
    })
