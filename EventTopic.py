class EventTopic:
    def __init__(self):
        self.message_id = None

    def set_id(self, message_id):
        self.message_id = message_id

    def get_id(self):
        return self.message_id


class Lunch(EventTopic):
    def __init__(self):
        super().__init__()

