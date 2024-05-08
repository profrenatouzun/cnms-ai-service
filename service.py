from openaihelper import OpenAiHelper
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

CLOUD_DOCS_DB_DIRECTORY = 'db/cloud/'
UZUN_DOCS_DB_DIRECTORY = 'db/uzun/'


def ask_question( openaihelper, prompt):
   
    languageVerificationMessages = [
        { "role": "user", "content": f"In one word, what language is the prompt: {prompt}"}
    ]

    languageResponse = openaihelper.getChatCompletion(
        temperature=0,
        messages=languageVerificationMessages,
        max_tokens=10,
        )

    print (f"Language Response: {languageResponse}");

    if not languageResponse.lower().startswith("portugues"):
        return {
              "prompt": prompt,
               "answer":"So sei responder em portugues. Por favor refaça sua pergunta no meu idioma"
        }
    
    subjectVerificationMessages = [
        { "role": "system", "content": f""" 
        You must verify the question and return just one letter in response. 
        If the subject of the question is something related with cloud computing then return 'C'.
        If the subject of the question is something related with the teacher Renato Gobet Uzun then return 'U',
        otherwise return 'N' """},
        {"role": "user", "content" : prompt}
    ]

    subjectResponse = openaihelper.getChatCompletion(
        temperature=0,
        messages=subjectVerificationMessages,
        max_tokens=1,
        )

    print (f"Subject Verification Response: {subjectResponse}");

    prompt = f"Answer in brazillian portuguese: {prompt}"


    if subjectResponse == "N":
        return {
              "prompt": prompt,
               "answer":"Só estou habilitado a responder perguntas sobre Computação em Nuvem ou sobre o Prof. Renato Gobet Uzun. Por favor refaça sua pergunta."
        }
    
    if subjectResponse == "C":
        #load docs from ChromaDb
        cloudDataVectordb = Chroma(persist_directory=CLOUD_DOCS_DB_DIRECTORY, embedding_function=openaihelper.getLangChainEmbeddings())
        #docs = cloudDataVectordb.similarity_search(PROMPT_QUESTION,k=3)
        
        print(f"Cloud Data Vector DB Size: {cloudDataVectordb._collection.count()}")

        chain = RetrievalQA.from_chain_type(openaihelper.getLangChainChatLlm(),
            retriever=cloudDataVectordb.as_retriever(search_kwargs={'k': 3}),
            chain_type="refine",
            return_source_documents=True,
        )
        result = chain.invoke({"query": prompt})
        return {
            "prompt": result['query'],
            "answer": result['result'],
            "references": list(map(lambda x: x.metadata, result['source_documents'])),
        }

    if subjectResponse == "U":
        #load docs from ChromaDb
        uzunDataVectordb = Chroma(persist_directory=UZUN_DOCS_DB_DIRECTORY, embedding_function=openaihelper.getLangChainEmbeddings())
        print(f"Uzun Data Vector DB Size: {uzunDataVectordb._collection.count()}")

        #docs = uzunDataVectordb.similarity_search(PROMPT_QUESTION,k=1)
        uzunDataRetriever = uzunDataVectordb.as_retriever(search_kwargs={'k': 1})
        chain = RetrievalQA.from_chain_type(openaihelper.getLangChainChatLlm(),
            retriever=uzunDataRetriever,
            return_source_documents=False,
            chain_type="map_reduce",
        )
        result = chain.invoke({"query": prompt})
        return {
            "prompt": result['query'],
            "answer": result['result'],
        }
