import requests
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from room.models.room import Room, RoomStatus
from room.game.main import Game


# def update_room_status(room):
#     url = "http://127.0.0.1:8000/api/host/" + str(room.pk)
#     headers = { 'Content-Type': 'application/json' }
#     data = requests.get(url, headers=headers, json=data).json()

#     return requests.post(url, headers=headers, json=data).json()


@receiver(post_save, sender=Room)
def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        print('room id: ',instance.pk, 'room status: ', instance.status)
    elif instance.status == RoomStatus.INITIALIZE:
        print('before calling.')
        game_thread = threading.Thread(target=Game(instance.pk).start())
        game_thread.start()
        print('after calling')