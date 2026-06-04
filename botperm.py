import yaml
import os

perms: dict[str, list[str]] = yaml.safe_load(open(os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'perms.yml')))

class Username(str): ...
class PermissionString(str): ...

def has_perm(user: Username, perm: PermissionString) -> bool: 
    return perm in perms.get(user, [])

def list_ns_perm(user: Username, perm_namespace) -> list[PermissionString]: 
    return [perm for perm in perms.get(user, {}) if perm.startswith(perm_namespace)]

def get_perm(user: Username, perm: PermissionString) -> str | None:
    for user_perm in perms.get(user, []):
        if user_perm.startswith(f"{perm}/"):
            return user_perm.split("/", 1)[1]
    return None

def list_with_perm(perm: PermissionString) -> list[Username]: 
    return [Username(user) for user, userp in perms.items() if perm in userp]
