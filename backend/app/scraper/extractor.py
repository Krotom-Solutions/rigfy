"""
Extrai specs técnicas estruturadas do texto livre dos anúncios da OLX.
Combina título + descrição para máxima cobertura.
"""
import re
import logging

logger = logging.getLogger(__name__)


def extrair_specs(titulo: str, descricao: str | None = None, categoria_forcada: str | None = None) -> dict:
    """
    Extrai specs técnicas de hardware do texto do anúncio.
    Retorna dict com todos os campos estruturados.
    """
    texto = f"{titulo} {descricao or ''}".lower()

    return {
        "categoria":       categoria_forcada or _extrair_categoria(texto),
        "marca":           _extrair_marca(texto),
        "cpu_fabricante":  _extrair_cpu_fabricante(texto),
        "cpu_linha":       _extrair_cpu_linha(texto),
        "cpu_geracao":     _extrair_cpu_geracao(texto),
        "ram_gb":          _extrair_ram(texto),
        "ram_tipo":        _extrair_ram_tipo(texto),
        "storage_gb":      _extrair_storage_gb(texto),
        "storage_tipo":    _extrair_storage_tipo(texto),
        "gpu":             _extrair_gpu(texto),
        "ano_fabricacao":  _extrair_ano(texto),
        "tem_nota_fiscal": _tem_nota_fiscal(texto),
        "tem_garantia":    _tem_garantia(texto),
        "specs_extraidas": True,
    }


def _extrair_categoria(texto: str) -> str | None:
    if any(x in texto for x in ['notebook', 'netbook', 'laptop']):
        return 'notebook'
    if any(x in texto for x in ['desktop', 'computador', 'pc gamer', 'torre']):
        return 'desktop'
    return None


def _extrair_marca(texto: str) -> str | None:
    marcas = {
        'dell': 'Dell', 'lenovo': 'Lenovo', 'hp': 'HP',
        'asus': 'Asus', 'acer': 'Acer', 'apple': 'Apple',
        'samsung': 'Samsung', 'positivo': 'Positivo',
        'multilaser': 'Multilaser', 'lg': 'LG', 'sony': 'Sony',
    }
    for chave, valor in marcas.items():
        if chave in texto:
            return valor
    return None


def _extrair_cpu_fabricante(texto: str) -> str | None:
    if any(x in texto for x in ['intel', 'core i', 'celeron', 'pentium', 'xeon']):
        return 'Intel'
    if any(x in texto for x in ['amd', 'ryzen', 'athlon', 'a10', 'a12']):
        return 'AMD'
    return None


def _extrair_cpu_linha(texto: str) -> str | None:
    padroes = [
        (r'core\s*i9', 'Core i9'),
        (r'core\s*i7', 'Core i7'),
        (r'core\s*i5', 'Core i5'),
        (r'core\s*i3', 'Core i3'),
        (r'ryzen\s*9', 'Ryzen 9'),
        (r'ryzen\s*7', 'Ryzen 7'),
        (r'ryzen\s*5', 'Ryzen 5'),
        (r'ryzen\s*3', 'Ryzen 3'),
        (r'celeron', 'Celeron'),
        (r'pentium', 'Pentium'),
    ]
    for padrao, nome in padroes:
        if re.search(padrao, texto):
            return nome
    return None


def _extrair_cpu_geracao(texto: str) -> str | None:
    # Intel: "10ª geração", "10a ger", "10th gen", "i5-10210u"
    match = re.search(
        r'(\d{1,2})(?:ª|a|°|th|st|nd|rd)?\s*(?:ger(?:a(?:ção|cao)?)?|gen(?:eration)?)',
        texto
    )
    if match:
        return match.group(1)

    # Pelo modelo do processador Intel (ex: i5-10210U → geração 10)
    match = re.search(r'i[3579]-(\d{1,2})\d{3}', texto)
    if match:
        return match.group(1)

    # AMD Ryzen série (ex: Ryzen 5 5600 → série 5000)
    match = re.search(r'ryzen\s*[3579]\s+(\d)(\d{3})', texto)
    if match:
        return f"{match.group(1)}000"

    return None


def _extrair_ram(texto: str) -> int | None:
    match = re.search(r'(\d+)\s*gb\s*(?:de\s*)?(?:ram|memória|memoria)', texto)
    if not match:
        match = re.search(r'(\d+)\s*gb', texto)
    if match:
        valor = int(match.group(1))
        # Valores válidos de RAM: 2, 4, 6, 8, 12, 16, 24, 32, 64
        if valor in (2, 4, 6, 8, 12, 16, 24, 32, 48, 64):
            return valor
    return None


def _extrair_ram_tipo(texto: str) -> str | None:
    if 'ddr5' in texto:
        return 'DDR5'
    if 'ddr4' in texto:
        return 'DDR4'
    if 'ddr3' in texto:
        return 'DDR3'
    return None


def _extrair_storage_gb(texto: str) -> int | None:
    # TB primeiro (mais específico)
    match = re.search(r'(\d+)\s*tb', texto)
    if match:
        return int(match.group(1)) * 1024

    # GB de storage — busca após palavras relacionadas a storage
    match = re.search(
        r'(\d+)\s*gb\s*(?:ssd|hdd|nvme|sata|disco|armazenamento|storage)',
        texto
    )
    if not match:
        # Busca padrões como "ssd 256gb" ou "256gb ssd"
        match = re.search(
            r'(?:ssd|hdd|nvme|sata|disco)\s*(\d+)\s*gb',
            texto
        )
    if match:
        valor = int(match.group(1))
        # Valores típicos de storage
        if valor in (32, 64, 120, 128, 240, 256, 480, 512, 1024, 2048):
            return valor
        # Aceita qualquer valor entre 32GB e 4TB
        if 32 <= valor <= 4096:
            return valor
    return None


def _extrair_storage_tipo(texto: str) -> str | None:
    if 'nvme' in texto or 'm.2' in texto:
        return 'SSD NVMe'
    if 'ssd' in texto and 'sata' in texto:
        return 'SSD SATA'
    if 'ssd' in texto:
        return 'SSD'  # tipo não especificado
    if 'hdd' in texto or 'hd ' in texto or 'disco rígido' in texto:
        return 'HDD'
    return None


def _extrair_gpu(texto: str) -> str | None:
    padroes_gpu = [
        r'rtx\s*\d{3,4}(?:\s*ti)?',
        r'gtx\s*\d{3,4}(?:\s*ti)?',
        r'rx\s*\d{3,4}(?:\s*xt)?',
        r'radeon\s*\w+',
        r'intel\s*(?:iris|uhd|hd)\s*\w*',
        r'nvidia\s*\w+',
    ]
    for padrao in padroes_gpu:
        match = re.search(padrao, texto)
        if match:
            return match.group(0).strip().upper()
    return None


def _extrair_ano(texto: str) -> int | None:
    match = re.search(r'\b(201[5-9]|202[0-4])\b', texto)
    return int(match.group(1)) if match else None


def _tem_nota_fiscal(texto: str) -> bool:
    return any(x in texto for x in ['nota fiscal', 'nf ', 'com nf', 'nfe'])


def _tem_garantia(texto: str) -> bool:
    return any(x in texto for x in ['garantia', 'warranty'])
