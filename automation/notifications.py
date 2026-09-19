"""Notification adapter boundary; no provider credentials live here."""
class NotificationSink:
    def send(self,message:str)->None: raise NotImplementedError
class NullNotificationSink(NotificationSink):
    def __init__(self): self.messages=[]
    def send(self,message): self.messages.append(message[:4000])
