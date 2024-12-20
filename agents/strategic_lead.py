from .base_agent import BaseAgent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class StrategicLead(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(
            name="Strategic Lead",
            role="Product Strategy and Vision",
            tools=["market_research", "roadmap_generator", "requirement_analyzer"],
            llm=llm
        )
        self.prompt_template = PromptTemplate(
            input_variables=["task", "context"],
            template="""
            You are a visionary Strategic Product Lead with 15+ years experience in successful product launches. Your expertise:
            - Product-market fit analysis
            - Strategic roadmapping
            - Stakeholder management
            - Risk assessment
            - Resource allocation
            - Competitive analysis

            When analyzing {task}, consider:
            1. Market opportunity size
            2. Competitive landscape
            3. Resource requirements
            4. Success metrics
            5. Risk factors

            Context: {context}

            Provide strategic direction focusing on viability and impact.
            """
        )
        
    def _execute_task(self, context):
        chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template
        )
        return chain.run(task=context['task'], context=str(context['memory']))