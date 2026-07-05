from pydantic import BaseModel, Field


class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = Field(..., description="Nome do produto", examples=["Cebola"])
    quantidade: int = Field(..., description="Quantidade esperada para o produto", examples=[100])
    valor: float = Field(..., description="Valor esperado para o produto", examples=[5.5])


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca,
        feita apenas com base no id do produto.
    """
    produto_id: int = Field(..., description="Id do produto")
