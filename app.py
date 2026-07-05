from flask import render_template
from flask_openapi3 import OpenAPI, Info, Tag

from model import Session, ConfiguracaoEstacionamento
from schemas import ConfiguracaoEstacionamentoSchema, apresenta_configuracao, ErrorSchema


info = Info(title="API Estacionamento", version="1.0.0")
app = OpenAPI(__name__, info=info)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
configuracao_tag = Tag(name="Configuração", description="Cadastro, visualização e atualização da configuração do estacionamento")


@app.get('/', tags=[home_tag])
def home():
    """Página inicial da aplicação
    """
    return render_template("home.html"), 200


@app.get('/configuracao', tags=[configuracao_tag],
         responses={"404": ErrorSchema})
def get_configuracao():
    """Retorna a configuração cadastrada do estacionamento
    """
    session = Session()
    configuracao = session.query(ConfiguracaoEstacionamento).first()
    if not configuracao:
        error_msg = "Configuração do estacionamento ainda não foi cadastrada :/"
        return {"message": error_msg}, 404
    return apresenta_configuracao(configuracao), 200


@app.post('/configuracao', tags=[configuracao_tag],
          responses={"409": ErrorSchema})
def add_configuracao(body: ConfiguracaoEstacionamentoSchema):
    """Cadastra a configuração do estacionamento (área, capacidade e preço por hora)

    Só é permitida uma única configuração cadastrada. Para alterá-la, utilize o PUT.
    """
    session = Session()
    if session.query(ConfiguracaoEstacionamento).first():
        error_msg = "Configuração do estacionamento já cadastrada, utilize o PUT para atualizá-la :/"
        return {"message": error_msg}, 409

    configuracao = ConfiguracaoEstacionamento(
        area=body.area,
        capacidade=body.capacidade,
        preco_hora=body.preco_hora
    )
    session.add(configuracao)
    session.commit()
    return apresenta_configuracao(configuracao), 200


@app.put('/configuracao', tags=[configuracao_tag],
         responses={"404": ErrorSchema})
def update_configuracao(body: ConfiguracaoEstacionamentoSchema):
    """Atualiza a configuração cadastrada do estacionamento
    """
    session = Session()
    configuracao = session.query(ConfiguracaoEstacionamento).first()
    if not configuracao:
        error_msg = "Configuração do estacionamento ainda não foi cadastrada :/"
        return {"message": error_msg}, 404

    configuracao.area = body.area
    configuracao.capacidade = body.capacidade
    configuracao.preco_hora = body.preco_hora
    session.commit()
    return apresenta_configuracao(configuracao), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
