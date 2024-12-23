from .base_agent import BaseAgent
from langchain_core.prompts import PromptTemplate
from typing import Optional, Any

class GrowthStrategist(BaseAgent):
    def __init__(self, llm: Optional[Any] = None):
        super().__init__(
            name="Growth Strategist",
            role="Growth and GTM Strategy",
            tools=["seo_analyzer", "funnel_designer", "market_analyzer"],
            llm=llm
        )
        self.prompt_template = PromptTemplate(
            input_variables=["task", "context"],
            template="""
            You are a Growth & GTM Strategist with expertise in:
            - Data-driven marketing strategies
            - SEO & SEM mastery
            - CRM implementation (Salesforce, HubSpot)
            - Marketing automation
            - Analytics (GA4, Mixpanel)
            - B2B/B2C funnel optimization
            - Content strategy

            For {task}, analyze:
            1. Customer acquisition channels
            2. CAC and LTV projections
            3. Market positioning
            4. Growth metrics
            5. Marketing tech stack

            Context: {context}

            Deliverables:
            1. Growth strategy
            2. Marketing funnel design
            3. Channel prioritization
            4. Marketing automation setup
            """
        )
        
    def _execute_task(self, context):
        return super()._execute_task(context)