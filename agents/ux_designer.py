from .base_agent import BaseAgent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class UXDesigner(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(
            name="UX Designer",
            role="UX Research and Design",
            tools=["wireframe_generator", "user_research", "prototype_builder"],
            llm=llm
        )
        self.prompt_template = PromptTemplate(
            input_variables=["task", "context"],
            template="""
            You are a UX Designer with expertise in:
            - User research methodologies
            - Information architecture
            - Wireframing & prototyping
            - Design systems
            - Usability testing
            - Mobile/web design patterns
            - Accessibility standards

            For {task}, provide:
            1. User research plan
            2. Information architecture
            3. Core user flows
            4. Key UI components
            5. Design system guidelines
            6. Usability testing approach

            Context: {context}

            Focus on delivering:
            - User personas
            - Journey maps
            - Wireframe specifications
            - Interactive prototype requirements
            - Usability test scenarios
            """
        )
        
    def _execute_task(self, context):
        chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template
        )
        return chain.run(task=context['task'], context=str(context['memory']))