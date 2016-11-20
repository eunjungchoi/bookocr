from django.shortcuts import render

def index(request):
	return render(request, 'bookscore_index.html')
