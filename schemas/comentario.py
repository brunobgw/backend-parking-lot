from typing import Optional

from pydantic import BaseModel, Field


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    autor: str = Field(..., description="Nome do autor do comentário", examples=["João"])
    texto: str = Field(..., description="Texto do comentário", examples=["Produto muito bom!"])
    n_estrela: Optional[int] = Field(None, description="Nota de 0 a 5 estrelas para o produto", examples=[5])
