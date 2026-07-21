from django.db import models

# Create your models here.
class Candidate(models.Model):
    id = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=100)
    total_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class VoteRecord(models.Model):
    mem_id = models.ForeignKey('member.event_member', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mem_id} voted for {self.name} at {self.timestamp}"

