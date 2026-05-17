import keyring


def resolve_token(project_name:str = "default", token: str | None = None) -> str:
    if token:
        return token

    stored_token = keyring.get_password("ionq", project_name)
    if not stored_token:
        raise ValueError(f"No stored token found for project '{project_name!r}', and no token provided.\n" 
                         f"Run: keyring.set_password('ionq', {project_name!r}, '<your-key>')")
    return stored_token

