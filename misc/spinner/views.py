from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from spinner import Spinner
from models import Word, Space, Relation
import signals


aResults = []
oSpinner = Spinner()
		
def index(oRequest):
	return HttpResponse("Hello World")
	
def search(oRequest):
	
	try:
		sQuery 		= oRequest.GET['q']
		
		if len(sQuery) == 0:
			raise ValueError
		
	except:
		return HttpResponse('Error: Invalid Query')
		
	else:
		bExtended	= 'opt_extended' in oRequest.GET.keys() and oRequest.GET['opt_extended'] == 'on'
		
		def callback(sApp, xData):
			return HttpResponse(sApp)
			
		kVariables = {
			'query': sQuery,
		}
			
		oSpinner.search(sQuery, ['boss'], [callback])
		
		return render_to_response('spinner/search.html', kVariables)
	
	
#
# RE
def results(oRequest):
	sQuery	= oRequest.GET['q']


	try:
			sQuery	= oRequest.GET['q']
			return HttpResponse(
				simplejson.dumps(Relation.objects.get_synonyms(sQuery))
			)

		
	except:
		raise
	
def synonyms(oRequest):
	
	try:
		sQuery		= oRequest.GET['q']

		if len(sQuery) == 0:
			raise ValueError, "Invalid Query"

	except:
		return HttpResponse('Error: Invalid Query')
		
	else:
		
		kSynonyms = Relation.objects.get_synonyms(sQuery.split(' '))
		return HttpResponse(
			simplejson.dumps(kSynonyms)
		)
	
