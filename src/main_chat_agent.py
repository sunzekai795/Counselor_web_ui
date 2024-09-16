from typing import List
from langchain.chains import LLMChain
from langchain.schema import SystemMessage,BaseMessage,AIMessage,HumanMessage
from langchain_core.language_models import BaseChatModel
from langchain.prompts import ChatPromptTemplate

class ChatAgent(object):
    def __init__(self,system_message:SystemMessage,chat_model:BaseChatModel,initial_chat_history:List[BaseMessage]=[]):
        self.system_message = system_message
        self.chat_model=chat_model
        self.initial_chat_history = [system_message]+initial_chat_history
        self.messageHistory = self.initial_chat_history
        

    def step(self,humanMessage:str,temperature:float=0.8,top_p:float=0.9):
        human_message = HumanMessage(content=humanMessage)
        self.messageHistory.append(human_message)
        response=self.chat_model(self.messageHistory)
        assert isinstance(response,AIMessage)
        self.messageHistory.append(response)
        return self.messageHistory

    def stream2(self,humanMessage:HumanMessage):
        self.messageHistory.append(humanMessage)
        response=""
        for chunk in self.chat_model.stream(self.messageHistory):
            response+=chunk.content
            yield chunk        
        AI_message=AIMessage(content=response)
        self.messageHistory.append(AI_message)
        return 

    def list_to_history(self, dia_history):
        try:
            self.messageHistory = [self.system_message]
            for i in range(0,len(dia_history),2):
                new_human = HumanMessage(content=dia_history[i])
                new_ai = AIMessage(content=dia_history[i+1])
                self.messageHistory.append(new_human)
                self.messageHistory.append(new_ai)
        except:
            pass
    
    def change_sys_msg(self):
        self.messageHistory[0] = self.system_message

    def get_history(self):
        return self.messageHistory

    def reset(self):
        self.messageHistory = [self.system_message]
