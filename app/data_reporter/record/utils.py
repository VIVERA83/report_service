def is_float_number(number: int | float) -> bool:
    integer = int(number)
    return (integer / 2) * 2 != number
