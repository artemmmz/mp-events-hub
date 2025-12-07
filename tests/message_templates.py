def build_status_message(
    actual_status: int,
    expected_status: int,
    details: str,
) -> str:
    return f"Status code: {actual_status}, but expected: {expected_status}, details: {details}"