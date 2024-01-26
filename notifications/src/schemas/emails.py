from pydantic import BaseModel


class InputPersonalFilmSelection(BaseModel):
	"""
	Данная модель предназначена для еженедельного
	оповещения пользователей персонально
	"""
	pass


class InputNewFilmsReleases(BaseModel):
	"""
	Данная модель предназначена для ежемесячного
	оповещения всех пользователей
	"""
	pass


class InputWelcomeMessage(BaseModel):
	"""
	Данная модель предназначена для оповещения
	пользователей, которые только что зарегистрировались
	"""
	pass
