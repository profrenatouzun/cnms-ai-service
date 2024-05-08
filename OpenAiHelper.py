from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI

CHAT_MODEL = "gpt-35-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"

class OpenAiHelper:

    def __init__(self, azureOpenAiKey, azureOpenAiUrl, azureOpenAiVersion):
        self.apiKey = azureOpenAiKey
        self.apiUrl = azureOpenAiUrl
        self.apiVersion = azureOpenAiVersion
        self.chatLlm = None
        self.embeddings = None

    def getEmbeddings(self):
        if not self.embeddings:
            self.buildEmbeddings()
        return self.embeddings          

    def buildEmbeddings(self):
        self.embeddings = AzureOpenAIEmbeddings(
            api_key=self.apiKey,
            api_version=self.apiVersion,
            azure_endpoint=self.apiUrl,
            model=EMBEDDING_MODEL,
        )

    def getChatLlm(self):
        if not self.chatLlm:
            self.buildChatLlm()
        return self.chatLlm           

    def buildChatLlm(self):
        self.chatLlm = AzureChatOpenAI(
            api_key=self.apiKey,
            api_version=self.apiVersion,
            azure_endpoint=self.apiUrl,
            azure_deployment=CHAT_MODEL,
        )

        