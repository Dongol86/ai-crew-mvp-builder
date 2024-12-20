from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

class BaseAgent:
    def __init__(self, name, role, tools=None, llm=None):
        self.name = name
        self.role = role
        self.tools = tools or []
        self.llm = llm
        self.memory = ConversationBufferMemory()
        self.prompt_template = None

    def process_task(self, task):
        context = {
            'task': task,
            'role': self.role,
            'memory': self.memory.load_memory_variables({})
        }
        return self._execute_task(context)

    def _execute_task(self, context):
        if not self.llm:
            raise ValueError(f"LLM not initialized for {self.name}")
        if not self.prompt_template:
            raise ValueError(f"Prompt template not initialized for {self.name}")

        chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template
        )
        return chain.run(context)