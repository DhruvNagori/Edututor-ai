# from langchain_core.messages import HumanMessage, AIMessage

# class ChatMemory:
#     def __init__(self):
#         self.history = []

#     def add_user(self, text: str):
#         self.history.append(HumanMessage(content=text))

#     def add_ai(self, text: str):
#         self.history.append(AIMessage(content=text))

#     def get(self):
#         return self.history


from langchain_core.messages import HumanMessage, AIMessage

class ChatMemory:
    def __init__(self):
        self.history = []

    def add_user(self, text: str):
        self.history.append(HumanMessage(content=text))

    def add_ai(self, text: str):
        self.history.append(AIMessage(content=text))

    def get(self):
        return self.history
    
    def clear(self):
        """Clear all conversation history"""
        self.history = []
    
    def get_last_n(self, n: int = 5):
        """Get last n messages for context window management"""
        return self.history[-n:] if len(self.history) > n else self.history