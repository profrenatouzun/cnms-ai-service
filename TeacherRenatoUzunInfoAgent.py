from OpenAiHelper import OpenAiHelper
from ChromaDbDataAgent import ChromaDbDataAgent

UZUN_DOCS_DB_DIRECTORY = 'db/uzun/'

class TeacherRenatoUzunInfoAgent (ChromaDbDataAgent):
    def __init__(self, openaihelper):
        super(TeacherRenatoUzunInfoAgent, self).__init__(
            UZUN_DOCS_DB_DIRECTORY, 
            openaihelper= openaihelper, 
            retrieverDocsListSize=1, 
            returnSources=False
            )
