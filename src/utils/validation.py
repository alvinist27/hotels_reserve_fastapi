def check_not_only_whitespace(user_input: str):
    if not user_input.strip():
        raise ValueError('Field cannot be empty or contain only whitespace')
    return user_input.strip()
