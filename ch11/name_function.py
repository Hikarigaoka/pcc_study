def get_formatted_name(first, last, middle=''):
    """읽기 좋은 전체 이름을 생성합니다."""

    if middle:
        full_name = f"{first} {middle} {last}"
    else:
        full_name = f"{first} {last}"
    
    return full_name.title()