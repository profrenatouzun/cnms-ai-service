from OpenAiHelper import OpenAiHelper
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

class ChromaDbDataAgent:

    def __init__(self, chromaDbDirectory, openaihelper, retrieverDocsListSize = 3, returnSources = False):
        self.chromaDbDirectory = chromaDbDirectory
        self.openaihelper = openaihelper
        self.retrieverDocsListSize = retrieverDocsListSize
        self.returnSources = returnSources
    

    def askQuestion(self, prompt):
        newPrompt = f"Answer in brazillian portuguese: {prompt}"

        #load docs from ChromaDb
        vectorDb = Chroma(persist_directory=self.chromaDbDirectory, embedding_function=self.openaihelper.getEmbeddings())
        retriever = vectorDb.as_retriever(search_kwargs={'k': self.retrieverDocsListSize})
        
        chain = RetrievalQA.from_chain_type(
            self.openaihelper.getChatLlm(),
            retriever=retriever,
            chain_type="refine",
            return_source_documents=self.returnSources,
        )
        result = chain.invoke({"query": newPrompt})
        
        output = {
            "answer": result['result'],
        }

        if self.returnSources and result['source_documents'] :
            output["references"] = list(map(lambda x: x.metadata, result['source_documents']))
        
        return output
