
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async
from .models import Candidate

class VoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'live_vote_group'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # 접속 시 현재 투표 상태 전송
        await self.send_vote_status()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        candidate_id = data.get('candidate_id')
        
        if candidate_id:
            await self.increment_vote(candidate_id)
            # 모든 유저에게 업데이트된 투표 결과 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'share_vote_status'}
            )

    async def share_vote_status(self, event):
        await self.send_vote_status()

    async def send_vote_status(self):
        votes_data = await self.get_current_votes()
        await self.send(text_data=json.dumps({'votes': votes_data}))

    @database_sync_to_async
    def increment_vote(self, candidate_id):
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.votes += 1
            candidate.save()
        except Candidate.DoesNotExist:
            pass

    @database_sync_to_async
    def get_current_votes(self):
        return list(Candidate.objects.values('id','mem_id', 'mem_Event','name', 'total_votes'))
    

    
