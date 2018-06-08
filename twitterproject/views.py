from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from . import friend
#for graphing
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image, io


from rest_framework.views import APIView
from rest_framework.response import Response

def home(request):
	return render(request, 'home.html')


def tweets(request):
 
	#get the handle from the input field
	person = friend.Friend(request.GET['twitter_handle'])


	pos_sent, neg_sent, nut_sent, tweets, likes = person.getSentiments()



	return render(request, 'tweets.html',{'username':person.twitter_handle,'tweets': tweets, 'likes': likes, 'positives': pos_sent,'negatives': neg_sent, 'neutrals': nut_sent})


def analysis(request):

	# Send buffer in a http response the the browser with the mime type image/png set
	#picture = HttpResponse(buffer.getvalue(), content_type="image/png")

	return render(request, 'analysis.html')



def get_data(requets, *args, **kwargs):
	data = {
		"sales": 100,
		"customers": 10,
	}
	return JsonResponse(data)

class ChartData(APIView):

	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		data = {
			"sales": 100,
			"customers": 10,
		}		
		return Response(data)