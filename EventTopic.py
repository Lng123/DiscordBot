from datetime import datetime

class EventTopic:
    def __init__(self, time_allowed=(60*5)):
        self.message_id = None
        self.time_allowed = time_allowed
        self.winner = None

    def set_id(self, message_id):
        self.message_id = message_id

    def get_id(self):
        return self.message_id

    def set_winner(self, winner):
        self.winner = winner

    def get_winner(self):
        return self.winner


class Lunch(EventTopic):
    def __init__(self, alarm_time="18:00"):
        super().__init__()
        self.alarm_time = alarm_time
        self.title_poll = f"Lunch poll for " \
                          f"{datetime.today().strftime('%Y-%m-%d')}"

    def get_alarm(self):
        return self.alarm_time

    def get_title_poll(self):
        return self.title_poll

    def get_title_results(self):
        return f"Lunch at {self.winner} on {self.alarm_time}"

# def main():
#     t1 = datetime.strptime("01:20", "%H:%M")
#     t2 = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")
#     diff = t2 - t1
#     print(diff)
#
# if __name__ == '__main__':
#     main()