from jinja2 import FileSystemLoader, Environment
from core.config import BASE_DIR

path = f'{BASE_DIR}/templates'
template_env = Environment(
	loader=FileSystemLoader(searchpath=path)
)
