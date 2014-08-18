from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages

# Decorators
from django.views.decorators.http import require_POST

# Models
from mapApp.models.incident import Incident
from mapApp.models.hazard import Hazard
from mapApp.models.theft import Theft

# Forms
from mapApp.forms.incident import IncidentForm
from mapApp.forms.hazard import HazardForm
from mapApp.forms.theft import TheftForm

from mapApp.views import alertUsers, indexContext


@require_POST
def postIncident(request):
	incidentForm = IncidentForm(request.POST)
	incidentForm.data = incidentForm.data.copy()
	
	# Convert coords to valid geometry
	try:
		incidentForm.data['geom'] = GEOSGeometry(incidentForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>No point was selected for this type of report.')
		return HttpResponseRedirect(reverse('mapApp:index')) 

	if incidentForm.is_valid():
		incident = incidentForm.save()
		alertUsers(request, incident)

		messages.success(request, '<strong>Thank you!</strong><br>Your incident marker was successfully added.')			
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(incident.latlngList()[0]),		\
				"lng":str(incident.latlngList()[1]),		\
				"zoom":str(18)								\
			})												\
		)) 
	else: # Show form errors 
		return render(request, 'mapApp/index.html', indexContext(request, incidentForm=incidentForm))

@require_POST
def postHazard(request):
	hazardForm = HazardForm(request.POST)
	hazardForm.data = hazardForm.data.copy()
	
	# Convert coords to valid geometry
	try :
		hazardForm.data['geom'] = GEOSGeometry(hazardForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>No point was selected for this type of report.')
		return HttpResponseRedirect(reverse('mapApp:index')) 

	if hazardForm.is_valid():
		hazard = hazardForm.save()
		alertUsers(request, hazard)
		
		messages.success(request, '<strong>Thank you!</strong><br>Your hazard marker was successfully added.')			
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(hazard.latlngList()[0]),		\
				"lng":str(hazard.latlngList()[1]),		\
				"zoom":str(18)								\
			})												\
		)) 

	else: # Show form errors 
		return render(request, 'mapApp/index.html', indexContext(request, hazardForm=hazardForm))

@require_POST
def postTheft(request):
	theftForm = TheftForm(request.POST)
	theftForm.data = theftForm.data.copy()
	
	# Convert coords to valid geometry
	try:
		theftForm.data['geom'] = GEOSGeometry(theftForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>No point was selected for this type of report.')
		return HttpResponseRedirect(reverse('mapApp:index')) 

	if theftForm.is_valid():
		theft = theftForm.save()
		alertUsers(request, theft)
		
		messages.success(request, '<strong>Thank you!</strong><br>Your theft marker was successfully added.')			
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(theft.latlngList()[0]),		\
				"lng":str(theft.latlngList()[1]),		\
				"zoom":str(18)								\
			})												\
		)) 

	else: # Show form errors 
		return render(request, 'mapApp/index.html', indexContext(request, theftForm=theftForm))