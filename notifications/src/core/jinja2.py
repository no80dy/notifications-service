from core.config import BASE_DIR
from jinja2 import Environment, FileSystemLoader

path = f"{BASE_DIR}/templates/"
template_env = Environment(loader=FileSystemLoader(searchpath=path))
