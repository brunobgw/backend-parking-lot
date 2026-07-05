from flask import request, send_from_directory, render_template
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError

from model import Session, Produto
from model.comentario import Comentario
from schemas import ProdutoSchema, ProdutoBuscaSchema, ComentarioSchema, ErrorSchema


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produto cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Página inicial da aplicação
    """
    return render_template("home.html"), 200


@app.get('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/x-icon')


@app.post('/add_produto', tags=[produto_tag],
           responses={"409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados
    """
    session = Session()
    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor
    )
    try:
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return render_template("produto.html", produto=produto), 200
    except IntegrityError:
        error_msg = "Produto de mesmo nome já salvo na base :/"
        return render_template("error.html", error_code=409, error_msg=error_msg), 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        print(str(e))
        return render_template("error.html", error_code=400, error_msg=error_msg), 400


@app.get('/get_produto/<produto_id>', tags=[produto_tag],
          responses={"404": ErrorSchema})
def get_produto(path: ProdutoBuscaSchema):
    """Busca um Produto a partir do id informado
    """
    session = Session()
    produto = session.query(Produto).filter(Produto.id == path.produto_id).first()
    if not produto:
        error_msg = "Produto não encontrado na base :/"
        return render_template("error.html", error_code=404, error_msg=error_msg), 404
    else:
        return render_template("produto.html", produto=produto), 200


@app.delete('/del_produto/<produto_id>', tags=[produto_tag],
             responses={"404": ErrorSchema})
def del_produto(path: ProdutoBuscaSchema):
    """Remove um Produto a partir do id informado
    """
    session = Session()
    count = session.query(Produto).filter(Produto.id == path.produto_id).delete()
    session.commit()
    if count == 1:
        return render_template("deletado.html", produto_id=path.produto_id), 200
    else:
        error_msg = "Produto não encontrado na base :/"
        return render_template("error.html", error_code=404, error_msg=error_msg), 404


@app.post('/add_comentario/<produto_id>', tags=[comentario_tag],
           responses={"404": ErrorSchema})
def add_comentario(path: ProdutoBuscaSchema, form: ComentarioSchema):
    """Adiciona um novo comentário ao Produto identificado pelo id informado
    """
    session = Session()
    produto = session.query(Produto).filter(Produto.id == path.produto_id).first()
    if not produto:
        error_msg = "Produto não encontrado na base :/"
        return render_template("error.html", error_code=404, error_msg=error_msg), 404

    comentario = Comentario(form.autor, form.texto, form.n_estrela)
    produto.adiciona_comentario(comentario)
    session.commit()
    return render_template("produto.html", produto=produto), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
