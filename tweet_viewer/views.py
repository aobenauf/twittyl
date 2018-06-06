from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def get_data(requets, *args, **kwargs):
	data = {
		"sales": 100,
		"customers": 10,
	}
	return JsonResponse(data):
