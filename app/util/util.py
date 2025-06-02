meses = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


def get_month_name(month_number):
    """Retorna o nome do mês correspondente ao número fornecido."""
    if 1 <= month_number <= 12:
        return meses[month_number - 1]
    else:
        raise ValueError("Número do mês deve estar entre 1 e 12.")
