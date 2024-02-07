from core.config import BASE_DIR
from jinja2 import Environment, FileSystemLoader

template_env = Environment(loader=FileSystemLoader(searchpath=f"{BASE_DIR}/templates/"))
