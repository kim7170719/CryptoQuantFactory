import logging

class EventEngine:
    def __init__(self):
        self.events = []
    def add_event(self, event):
        self.events.append(event)
    def process(self, data):
        try:
            for event in self.events:
                data = event(data)
            return data
        except Exception as e:
            logging.error(f'EventEngine process error: {e}')
            return data
