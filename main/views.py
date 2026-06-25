from django.shortcuts import render
from django.http import HttpResponse
from board.models import board
# Create your views here.
def index(request):
    board_list = board.objects.all().order_by('-car_idx')[:5] # 최신 게시물 5개 가져오기    
    return render(request, 'main/main.html', {'board_list': board_list})