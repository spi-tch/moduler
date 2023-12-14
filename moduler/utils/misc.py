def convert_to_str_dict(dictionary: dict) -> dict:
    return {str(key): str(value) for key, value in dictionary.items()}

