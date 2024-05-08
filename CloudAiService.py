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
        
        chain = prompt | llm | self.getTagArguments | self.callAgent

        output = chain.invoke({"promptText": promptText})
        output["prompt"] = promptText
        return output
        
        

    def getTagArguments(self, jsonData):
        s = jsonData.additional_kwargs["function_call"]["arguments"]
        s = s.replace("(","").replace(")", "")
        s2 = dirtyjson.loads(s)
        return s2


    def callAgent(self, promptTags):
        
        if not promptTags["language"].lower() == "pt":
            return { "answer": LANGUAGE_ERROR_MESSAGE, "tags": promptTags }
        
        subject = promptTags["subject"].lower();
        agent = None
        
        if subject == "cloud computing":
            agent = CloudTeacherAgent(openaihelper=self.openaihelper)
        
        elif subject == "teacher renato":
            agent = TeacherRenatoUzunInfoAgent(openaihelper=self.openaihelper)
        
        else:
            return { "answer": SUBJECT_ERROR_MESSAGE, "tags": promptTags }
            
        output = agent.askQuestion(promptTags["standaloneQuestion"])
        output["tags"] = promptTags
        return output
        