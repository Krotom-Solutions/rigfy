from datetime import datetime
from pydantic import BaseModel, field_validator


class AnuncioRaw(BaseModel):
    """Dados brutos vindos do parser — antes da extração de specs."""

    olx_id: str
    url: str
    titulo: str
    descricao: str | None = None
    preco_texto: str | None = None
    preco: float | None = None
    localizacao: str | None = None
    data_publicacao_texto: str | None = None

    @field_validator("preco_texto")
    @classmethod
    def limpar_preco(cls, v):
        return v.strip() if v else v


class AnuncioDB(AnuncioRaw):
    id: int
    coletado_em: datetime
    specs_extraidas: bool

    model_config = {"from_attributes": True}
