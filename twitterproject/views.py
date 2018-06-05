from django.http import HttpResponse
from django.shortcuts import render
from . import friend
#for graphing
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image, io

def home(request):
	return render(request, 'home.html')


def tweets(request):
 
	#get the handle from the input field
	person = friend.Friend(request.GET['twitter_handle'])


	pos_sent, neg_sent, nut_sent, tweets, likes = person.getSentiments()



	return render(request, 'tweets.html',{'username':person.twitter_handle,'tweets': tweets, 'likes': likes, 'positives': pos_sent,'negatives': neg_sent, 'neutrals': nut_sent})


def analysis(request):
	# Construct the graph
	x = arange(0, 2*pi, 0.01)
	s = cos(x)**2
	plot(x, s)

	xlabel('xlabel(X)')
	ylabel('ylabel(Y)')
	title('Simple Graph!')
	grid(True)

	# Store image in a string buffer
	buffer = io.BytesIO()
	canvas = pylab.get_current_fig_manager().canvas
	canvas.draw()
	pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())

	#CAN I SAVE A DIFFERENT WAY
	pilImage.save('/media/analysis.png', "PNG")
	#pylab.close()

	# Send buffer in a http response the the browser with the mime type image/png set
	#picture = HttpResponse(buffer.getvalue(), content_type="image/png")

	return render(request, 'analysis.html')

	#this link might be helpful
	#https://stackoverflow.com/questions/30531990/matplotlib-into-a-django-template

# def getimage(request):
#     # Construct the graph
#     x = arange(0, 2*pi, 0.01)
#     s = cos(x)**2
#     plot(x, s)

#     xlabel('xlabel(X)')
#     ylabel('ylabel(Y)')
#     title('Simple Graph!')
#     grid(True)

#     # Store image in a string buffer
#     buffer = StringIO.StringIO()
#     canvas = pylab.get_current_fig_manager().canvas
#     canvas.draw()
#     pilImage = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
#     pilImage.save(buffer, "PNG")
#     pylab.close()

#     # Send buffer in a http response the the browser with the mime type image/png set
#     return HttpResponse(buffer.getvalue(), mimetype="image/png")	