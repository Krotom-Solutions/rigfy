from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, Boolean, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Anuncio(Base):
    __tablename__ = "anuncios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Identificação
    olx_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    plataforma: Mapped[str] = mapped_column(String(50), default="olx")

    # Dados brutos do anúncio
    titulo: Mapped[str] = mapped_column(String(300), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    preco_texto: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preco: Mapped[float | None] = mapped_column(Float, nullable=True)
    localizacao: Mapped[str | None] = mapped_column(String(200), nullable=True)
    data_publicacao_texto: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Specs extraídas (resultado do extractor.py)
    categoria: Mapped[str | None] = mapped_column(String(50), nullable=True)    # notebook, desktop
    marca: Mapped[str | None] = mapped_column(String(100), nullable=True)

    cpu_fabricante: Mapped[str | None] = mapped_column(String(50), nullable=True)   # Intel, AMD
    cpu_linha: Mapped[str | None] = mapped_column(String(50), nullable=True)         # Core i5, Ryzen 7
    cpu_geracao: Mapped[str | None] = mapped_column(String(20), nullable=True)       # 10, 11, 12...

    ram_gb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ram_tipo: Mapped[str | None] = mapped_column(String(20), nullable=True)          # DDR3, DDR4, DDR5

    storage_gb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    storage_tipo: Mapped[str | None] = mapped_column(String(20), nullable=True)      # HDD, SSD SATA, NVMe

    gpu: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # GPU specs e lançamento
    gpu_vram_gb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gpu_memoria_tipo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ano_lancamento: Mapped[int | None] = mapped_column(Integer, nullable=True)

    ano_fabricacao: Mapped[int | None] = mapped_column(Integer, nullable=True)

    tem_nota_fiscal: Mapped[bool] = mapped_column(Boolean, default=False)
    tem_garantia: Mapped[bool] = mapped_column(Boolean, default=False)

    # Controle interno
    specs_extraidas: Mapped[bool] = mapped_column(Boolean, default=False)
    coletado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (
        Index("ix_anuncios_olx_id", "olx_id"),
        Index("ix_anuncios_coletado_em", "coletado_em"),
        Index("ix_anuncios_preco", "preco"),
        Index("ix_anuncios_ram_gb", "ram_gb"),
        Index("ix_anuncios_cpu_linha", "cpu_linha"),
    )
