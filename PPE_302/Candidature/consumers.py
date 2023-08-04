



from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Traitez les données reçues du client WebSocket
        # et renvoyez les mises à jour des notifications
        # à travers le WebSocket

        # Exemple de renvoi des messages de notification existants
        messages = [...]  # Obtenez les messages de notification
        await self.send(text_data="\n".join(messages))

