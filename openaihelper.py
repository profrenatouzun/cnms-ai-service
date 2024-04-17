from openai import AzureOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI

CHAT_MODEL = "gpt-35-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"

class OpenAiHelper:

    def __init__(self, azureOpenAiKey, azureOpenAiUrl, azureOpenAiVersion):
        self.apiKey = azureOpenAiKey
        self.apiUrl = azureOpenAiUrl
        self.apiVersion = azureOpenAiVersion
        self.llm = None
        self.langChainChatLlm = None
        self.langChainEmbedding = None

    def getChatCompletion(self, messages, temperature = 0, max_tokens=0):
        if self.llm is None:
            self.buildLlm()
 
        response = self.llm.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def buildLlm(self):
        self.llm = AzureOpenAI(
            api_key=self.apiKey,
            api_version=self.apiVersion,
            azure_endpoint=self.apiUrl,
        )

    def getLangChainEmbeddings(self):
        if not self.langChainEmbedding:
            self.buildLangChainEmbeddings()
        return self.langChainEmbedding          

    def buildLangChainEmbeddings(self):
        self.langChainEmbedding = AzureOpenAIEmbeddings(
            api_key=self.apiKey,
            api_version=self.apiVersion,
            azure_endpoint=self.apiUrl,
            model=EMBEDDING_MODEL,
        )

    def getLangChainChatLlm(self):
        if not self.langChainChatLlm:
            self.buildLangChainChatLlm()
        return self.langChainChatLlm           

    def buildLangChainChatLlm(self):
        self.langChainChatLlm = AzureChatOpenAI(
            api_key=self.apiKey,
            api_version=self.apiVersion,
            azure_endpoint=self.apiUrl,
            azure_deployment=CHAT_MODEL,
        )

        