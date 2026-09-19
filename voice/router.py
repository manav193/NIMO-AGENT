"""Voice-to-Agent bridge. No tool execution happens in the voice layer."""
class VoiceRouter:
    def __init__(self,agent_handler): self.agent_handler=agent_handler
    def handle(self,text:str):
        return self.agent_handler(text)
