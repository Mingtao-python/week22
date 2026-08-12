ALLOWED_ROLES = {"student", "teacher", "admin"}


def can_access_document(user_role: str, document_meta: dict) -> bool:
    role = (user_role or "student").lower()
    if role not in ALLOWED_ROLES:
        return False

    if document_meta.get("private") is True and role != "admin":
        return False

    allowed_roles = document_meta.get("allowed_roles") or ["student", "teacher", "admin"]
    return role in set(allowed_roles)


def filter_documents_for_role(documents: list, user_role: str):
    role = (user_role or "student").lower()
    return [doc for doc in documents if can_access_document(role, doc)]
