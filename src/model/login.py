import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

schema_login	= {
	"type":	"object",
	"properties": {
		"email": {
			"type": "email"
		},
		"senha": {
			"type": "string"
		},
		"level": {
			"type": "string"
		}
	},
	"required": [
		"email",
		"senha",
		"level"
	]
}

class LoginType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_login)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Login(DynamicDocument):
	email	= EmailField(required=True)
	hash	= StringField(required=True)
	level	= StringField(required=True)
	
	meta = { "db_alias": "auth" }
