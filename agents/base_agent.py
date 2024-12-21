import logging
from typing import Dict, List, Optional, Any
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

class BaseAgent:
    def __init__(self, name: str, role: str, tools: Optional[List] = None, llm: Optional[BaseLanguageModel] = None):
        """
        Initialize the BaseAgent with a name, role, tools, and an optional LLM.
        
        :param name: Name of the agent
        :param role: Role of the agent
        :param tools: List of tools available to the agent
        :param llm: Language model chain for the agent
        """
        self.name = name
        self.role = role
        self.tools = tools or []
        self.llm = llm
        self.messages = []
        self.prompt_template = PromptTemplate(input_variables=["task", "context"], template="{task} {context}")
        self.output_parser = StrOutputParser()

    def process_task(self, task) -> str:
        """
        Process a given task using the agent's role and memory.
        
        :param task: Task to be processed
        :return: Result of the task processing
        """
        if isinstance(task, dict):
            context = task
            context['role'] = self.role
            context['memory'] = self.memory.load_memory_variables({})
        else:
            context = {
                'task': task,
                'role': self.role,
                'memory': self.memory.load_memory_variables({})
            }
        return self._execute_task(context)

    def _execute_task(self, context: Dict) -> str:
        """
        Execute the task using the context provided.
        
        :param context: Context for task execution
        :return: Result of the task execution
        """
        if not self.llm or not self.prompt_template:
            raise ValueError(f"LLM or prompt template not initialized for {self.name}")

        try:
            # Modern LangChain chain composition
            chain = self.prompt_template | self.llm | self.output_parser
            
            task_input = str(context.get('task', context))
            context_input = str(context.get('context', ''))
            
            response = chain.invoke({
                "task": task_input,
                "context": context_input
            })
            
            # Store interaction
            self.messages.extend([
                HumanMessage(content=task_input),
                AIMessage(content=response)
            ])
            
            return response
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            logging.error(error_msg)
            return error_msg

    def execute(self):
        raise NotImplementedError("Subclasses must implement execute method")