

from django.db import models
from datetime import timezone
from django.utils import timezone
# Create your models here.
   
class board(models.Model):
    car_idx = models.AutoField(primary_key=True,) #자동 증가
    car_name = models.CharField(max_length=100)
    car_order = models.CharField(max_length=100)
    car_field = models.CharField(max_length=30)
    car_year = models.CharField(max_length=4)
    car_day = models.CharField(max_length=100)
    car_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    car_url = models.CharField(max_length=100, blank=True, null=True)
    car_size_h = models.IntegerField(blank=True, null=True)
    car_size_w = models.IntegerField(blank=True, null=True)
    car_check = models.CharField(max_length=3, blank=True, null=True)
    car_readnum = models.IntegerField(default=0)
    car_content = models.CharField(max_length=500 ,blank=True, null=True)
    car_image = models.FileField(upload_to='boardimg/', max_length=100, blank=True, null=True)
    car_choo = models.IntegerField(blank=True, null=True)
    car_soonwe = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'board'
        verbose_name = '행사'
        verbose_name_plural = '행사'
        ordering = ['-car_idx']

    def __str__(self):
        return self.car_name
    
    

    
    



