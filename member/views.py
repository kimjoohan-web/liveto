from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'member/index.html')


def member_input(request):
    return render(request, 'member/member_input.html')