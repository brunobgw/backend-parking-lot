from flask import render_template
from flask_openapi3 import OpenAPI, Info, Tag

from model import Session, ConfiguracaoEstacionamento, Vaga
from schemas import (
    ConfiguracaoEstacionamentoSchema, ConfiguracaoEstacionamentoPatchSchema, apresenta_configuracao,
    VagaBuscaSchema, VagaOcupacaoSchema, apresenta_vaga, apresenta_vagas,
    ErrorSchema
)


info = Info(title="API Estacionamento", version="1.0.0")
app = OpenAPI(__name__, info=info)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
configuracao_tag = Tag(name="Configuração", description="Cadastro, visualização e atualização da configuração do estacionamento")
vaga_tag = Tag(name="Vaga", description="Visualização, ocupação e liberação das vagas do estacionamento")


def sincroniza_vagas(session, capacidade: int):
    """ Garante que existam exatamente `capacidade` vagas numeradas.

    Cria vagas novas (livres) quando a capacidade aumenta. Quando a
    capacidade diminui, remove vagas livres a partir do maior número.
    Retorna uma mensagem de erro caso não seja possível reduzir a
    capacidade por haver vagas ocupadas demais.
    """
    vagas = session.query(Vaga).order_by(Vaga.numero).all()
    total_atual = len(vagas)

    if capacidade > total_atual:
        for numero in range(total_atual + 1, capacidade + 1):
            session.add(Vaga(numero=numero))
        return None

    if capacidade < total_atual:
        ocupadas = [vaga for vaga in vagas if vaga.status == "ocupada"]
        if len(ocupadas) > capacidade:
            return (f"Não é possível reduzir a capacidade para {capacidade}: "
                    f"existem {len(ocupadas)} vaga(s) ocupada(s) :/")

        livres = sorted((vaga for vaga in vagas if vaga.status == "livre"),
                         key=lambda vaga: vaga.numero, reverse=True)
        for vaga in livres[:total_atual - capacidade]:
            session.delete(vaga)
        return None

    return None


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
    As vagas numeradas são criadas automaticamente de acordo com a capacidade.
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
    sincroniza_vagas(session, body.capacidade)
    session.commit()
    return apresenta_configuracao(configuracao), 200


@app.put('/configuracao', tags=[configuracao_tag],
         responses={"404": ErrorSchema, "409": ErrorSchema})
def update_configuracao(body: ConfiguracaoEstacionamentoSchema):
    """Atualiza a configuração cadastrada do estacionamento

    Ao alterar a capacidade, as vagas numeradas são ajustadas automaticamente:
    vagas novas são criadas se a capacidade aumentar, e vagas livres são
    removidas (a partir do maior número) se a capacidade diminuir.
    """
    session = Session()
    configuracao = session.query(ConfiguracaoEstacionamento).first()
    if not configuracao:
        error_msg = "Configuração do estacionamento ainda não foi cadastrada :/"
        return {"message": error_msg}, 404

    erro_msg = sincroniza_vagas(session, body.capacidade)
    if erro_msg:
        session.rollback()
        return {"message": erro_msg}, 409

    configuracao.area = body.area
    configuracao.capacidade = body.capacidade
    configuracao.preco_hora = body.preco_hora
    session.commit()
    return apresenta_configuracao(configuracao), 200


@app.patch('/configuracao', tags=[configuracao_tag],
           responses={"404": ErrorSchema, "409": ErrorSchema})
def patch_configuracao(body: ConfiguracaoEstacionamentoPatchSchema):
    """Atualiza parcialmente a configuração cadastrada do estacionamento

    Apenas os campos informados no corpo da requisição são alterados (por
    exemplo, ajustar só o preço por hora). Ao informar a capacidade, as vagas
    numeradas são ajustadas automaticamente, seguindo a mesma regra do PUT.
    """
    session = Session()
    configuracao = session.query(ConfiguracaoEstacionamento).first()
    if not configuracao:
        error_msg = "Configuração do estacionamento ainda não foi cadastrada :/"
        return {"message": error_msg}, 404

    if body.capacidade is not None:
        erro_msg = sincroniza_vagas(session, body.capacidade)
        if erro_msg:
            session.rollback()
            return {"message": erro_msg}, 409
        configuracao.capacidade = body.capacidade

    if body.area is not None:
        configuracao.area = body.area
    if body.preco_hora is not None:
        configuracao.preco_hora = body.preco_hora

    session.commit()
    return apresenta_configuracao(configuracao), 200


@app.delete('/configuracao', tags=[configuracao_tag],
            responses={"404": ErrorSchema, "409": ErrorSchema})
def delete_configuracao():
    """Remove a configuração cadastrada do estacionamento e todas as suas vagas

    Não é permitido remover a configuração enquanto houver vagas ocupadas.
    """
    session = Session()
    configuracao = session.query(ConfiguracaoEstacionamento).first()
    if not configuracao:
        error_msg = "Configuração do estacionamento ainda não foi cadastrada :/"
        return {"message": error_msg}, 404

    ocupadas = session.query(Vaga).filter(Vaga.status == "ocupada").count()
    if ocupadas > 0:
        error_msg = f"Não é possível remover a configuração: existem {ocupadas} vaga(s) ocupada(s) :/"
        return {"message": error_msg}, 409

    session.query(Vaga).delete()
    session.delete(configuracao)
    session.commit()
    return {"message": "Configuração do estacionamento removida com sucesso"}, 200


@app.get('/vagas', tags=[vaga_tag])
def get_vagas():
    """Lista todas as vagas do estacionamento
    """
    session = Session()
    vagas = session.query(Vaga).order_by(Vaga.numero).all()
    return apresenta_vagas(vagas), 200


@app.get('/vagas/<numero>', tags=[vaga_tag],
         responses={"404": ErrorSchema})
def get_vaga(path: VagaBuscaSchema):
    """Retorna os dados de uma vaga a partir do número informado
    """
    session = Session()
    vaga = session.query(Vaga).filter(Vaga.numero == path.numero).first()
    if not vaga:
        error_msg = "Vaga não encontrada :/"
        return {"message": error_msg}, 404
    return apresenta_vaga(vaga), 200


@app.put('/vagas/<numero>/ocupar', tags=[vaga_tag],
         responses={"404": ErrorSchema, "409": ErrorSchema})
def ocupar_vaga(path: VagaBuscaSchema, body: VagaOcupacaoSchema):
    """Ocupa uma vaga livre com a placa do veículo informado
    """
    session = Session()
    vaga = session.query(Vaga).filter(Vaga.numero == path.numero).first()
    if not vaga:
        error_msg = "Vaga não encontrada :/"
        return {"message": error_msg}, 404
    if vaga.status == "ocupada":
        error_msg = "Vaga já está ocupada :/"
        return {"message": error_msg}, 409

    vaga.ocupar(body.placa)
    session.commit()
    return apresenta_vaga(vaga), 200


@app.put('/vagas/<numero>/liberar', tags=[vaga_tag],
         responses={"404": ErrorSchema, "409": ErrorSchema})
def liberar_vaga(path: VagaBuscaSchema):
    """Libera uma vaga ocupada
    """
    session = Session()
    vaga = session.query(Vaga).filter(Vaga.numero == path.numero).first()
    if not vaga:
        error_msg = "Vaga não encontrada :/"
        return {"message": error_msg}, 404
    if vaga.status == "livre":
        error_msg = "Vaga já está livre :/"
        return {"message": error_msg}, 409

    vaga.liberar()
    session.commit()
    return apresenta_vaga(vaga), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
