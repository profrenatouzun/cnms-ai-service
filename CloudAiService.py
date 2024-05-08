from OpenAiHelper import OpenAiHelper
from PromptTagging import promptTaggingOpenAIFunctionTemplate
from CloudTeacherAgent import CloudTeacherAgent
from TeacherRenatoUzunInfoAgent import TeacherRenatoUzunInfoAgent
from langchain.prompts import ChatPromptTemplate
import dirtyjson

LANGUAGE_ERROR_MESSAGE = "Só sei responder em português. Por favor refaça sua pergunta no meu idioma"
SUBJECT_ERROR_MESSAGE = "Só estou habilitado a responder perguntas sobre Computação em Nuvem ou sobre o Prof. Renato Gobet Uzun. Por favor refaça sua pergunta."

class CloudAiService:
    def __init__(self, openaihelper):
            self.openaihelper = openaihelper

    def askQuestion(self, promptText):
        tagging_functions = [promptTaggingOpenAIFunctionTemplate]
    
        llm = self.openaihelper.getChatLlm().bind(functions= tagging_functions, function_call={"name": "PromptTagging"});
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Think carefully, and then tag the text as instructed"),
            ("user", "{promptText}")
        ])        
        
        chain = prompt | llm | self.getArguments | self.callAgent

        return chain.invoke({"promptText": promptText})
        

    def getArguments(self, jsonData):
        s = jsonData.additional_kwargs["function_call"]["arguments"]
        s = s.replace("(","").replace(")", "")
        s2 = dirtyjson.loads(s)
        print(s)
        return s2


    def callAgent(self, promptData):
        
        if not promptData["language"].lower().startswith("portugues") and not promptData["language"].lower() == "pt":
            return { "prompt": promptData["standaloneQuestion"], "answer": LANGUAGE_ERROR_MESSAGE }
        
        subject = promptData["subject"].lower();
        agent = None
        
        if subject == "cloud computing":
            agent = CloudTeacherAgent(openaihelper=self.openaihelper)
        
        elif subject == "teacher renato":
            agent = TeacherRenatoUzunInfoAgent(openaihelper=self.openaihelper)
        
        else:
            return { "prompt": promptData["standaloneQuestion"], "answer": SUBJECT_ERROR_MESSAGE }
            
        return agent.askQuestion(promptData["standaloneQuestion"])
        