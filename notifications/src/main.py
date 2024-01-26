import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from faststream.rabbit import RabbitBroker
from contextlib import asynccontextmanager

from warehouse import rabbitmq
from api.v1 import emails
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
	rabbitmq.rabbitmq_broker = RabbitBroker(
		host=settings.rabbitmq_host,
		port=settings.rabbitmq_port,
		login=settings.rabbitmq_login,
		password=settings.rabbitmq_password
	)
	await rabbitmq.rabbitmq_broker.connect()
	await rabbitmq.configure_rabbit_exchange()
	await rabbitmq.configure_rabbit_queue()
	yield
	await rabbitmq.rabbitmq_broker.close()


app = FastAPI(
	description='Сервис нотификаций',
	version='0.0.0',
	title=settings.project_name,
	docs_url='/notifications/api/openapi',
	openapi_url='/notifications/api/openapi.json',
	lifespan=lifespan
)


app.include_router(emails.router, tags=['kafka', ])

templates = Jinja2Templates(directory='templates')


@app.get('/new-films-releases', response_class=HTMLResponse)
async def check(request: Request):
	return templates.TemplateResponse(
		request=request,
		name='new-films-releases.html',
		context={
			'username': 'Awesome user',
			'film_count': 20,
			'serial_count': 8,
			'month': 'Февраль',
			'user_films_count': 1
		}
	)


if __name__ == '__main__':
	uvicorn.run(
		'main:app',
		host='0.0.0.0',
		port=8000,
		reload=True
	)
