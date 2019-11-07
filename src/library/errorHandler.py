import	hug
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_404, HTTP_502
import traceback

def handleError(response, e):
	print("Error: ", e)
	print(traceback.format_exc())
	type =  e.__class__.__name__
	if (type == 'DoesNotExist'):
		response.status = HTTP_404
		return { "error": "not_found" }
	else:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
