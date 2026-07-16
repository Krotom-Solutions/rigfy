from datetime import datetime
from pydantic import BaseModel


# ─── Schemas de resposta para /listings ──────────────────────────────────────

class AnuncioListItem(BaseModel):
    """Item resumido para listagem."""
    id: int
    olx_id: str
    url: str
    titulo: str
    preco: float | None
    preco_texto: str | None
    localizacao: str | None
    categoria: str | None
    marca: str | None
    cpu_linha: str | None
    cpu_geracao: str | None
    ram_gb: int | None
    storage_gb: int | None
    storage_tipo: str | None
    gpu: str | None
    tem_nota_fiscal: bool
    tem_garantia: bool
    coletado_em: datetime

    model_config = {"from_attributes": True}


class ListingsResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: list[AnuncioListItem]


# ─── Schemas de resposta para /stats/mercado ──────────────────────────────────

class EstatisticaGrupo(BaseModel):
    grupo: str
    total_anuncios: int
    preco_minimo: float | None
    preco_medio: float | None
    preco_maximo: float | None
    preco_mediano: float | None


class MercadoStatsResponse(BaseModel):
    total_anuncios: int
    total_com_preco: int
    por_categoria: list[EstatisticaGrupo]
    por_cpu_linha: list[EstatisticaGrupo]
    por_ram_gb: list[EstatisticaGrupo]
    por_marca: list[EstatisticaGrupo]


# ─── Schemas para /price/predict ─────────────────────────────────────────────

class PriceRequest(BaseModel):
    categoria: str | None = None          # "notebook" | "desktop"
    marca: str | None = None
    cpu_linha: str | None = None          # "Core i5" | "Ryzen 5" etc.
    cpu_geracao: str | None = None
    ram_gb: int | None = None
    storage_gb: int | None = None
    storage_tipo: str | None = None       # "SSD" | "SSD NVMe" | "HDD"
    gpu: str | None = None
    tem_nota_fiscal: bool = False
    tem_garantia: bool = False


class PriceResponse(BaseModel):
    preco_estimado: float | None
    preco_minimo: float | None
    preco_maximo: float | None
    preco_mediano: float | None
    total_anuncios_similares: int
    confianca: str                         # "alta" | "media" | "baixa" | "insuficiente"
    filtros_usados: dict
