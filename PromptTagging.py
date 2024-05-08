from pydantic import BaseModel, Field

class PromptTagging (BaseModel):
    "Tag the prompt text with particular info."
    language: str = Field(description="language of prompt text (should be ISO 639-1 code)")
    subject: str = Field(description="subject of prompt text, should be `Cloud Computing`, `Teacher Renato`, or `Other`")
    standaloneQuestion: str = Field(description="Standalone question of prompt text")


promptTaggingOpenAIFunctionTemplate= {
    "name": "PromptTagging",
    "description": "Tag the prompt text with particular info.", 
    "parameters": {
        "properties": {
            "language": {
                "description": "language of prompt text (should be ISO 639-1 code)",
                "type": "string"
            },
            "subject": {
                "description": "subject of prompt text, should be `Cloud Computing`, `Teacher Renato`, or `Other`",
                "type": "string",
                "enum": ["Cloud Computing", "Teacher Renato", "Other"]
            },
            "standaloneQuestion": {
                "description": "Standalone question of prompt text", 
                "type": "string"
            }
        }, 
        "required": ["language", "subject", "standaloneQuestion"], 
        "type": "object"
    }
}