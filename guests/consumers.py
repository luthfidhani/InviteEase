import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GuestConsumer(AsyncWebsocketConsumer):
    """
    * Desk connects → group: screen_<screen_id>
    * Screen connects → same group
    * Messages echo'd for now
    """

    async def connect(self):
        # Extract param from URL
        self.screen_id = self.scope["url_route"]["kwargs"].get("screen_id")
        self.desk_id = self.scope["url_route"]["kwargs"].get("desk_id")

        # Decide group name
        if self.screen_id:
            self.group_name = f"screen_{self.screen_id}"
        elif self.desk_id:
            # For desk we still join its mapped screen group later;
            # for demo, join "desk_x" just to echo
            self.group_name = f"screen_{self.desk_id}"
        else:
            # Unknown URL → reject
            await self.close()
            return

        # Join channel layer group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket → broadcast to group
    async def receive(self, text_data=None, **kwargs):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "group.message",
                **json.loads(text_data),
            },
        )

    # Receive from group → send to WebSocket
    async def group_message(self, event):
        await self.send(text_data=json.dumps(event))

