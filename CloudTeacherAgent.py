from OpenAiHelper import OpenAiHelper
from ChromaDbDataAgent import ChromaDbDataAgent

CLOUD_DOCS_DB_DIRECTORY = 'db/cloud/'

class CloudTeacherAgent (ChromaDbDataAgent):
    def __init__(self, openaihelper):
        super(CloudTeacherAgent, self).__init__(
            CLOUD_DOCS_DB_DIRECTORY,
            openaihelper= openaihelper,
            retrieverDocsListSize=3,
            returnSources=True
            )
