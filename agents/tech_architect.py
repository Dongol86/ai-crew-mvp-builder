from .base_agent import BaseAgent
from langchain_core.prompts import PromptTemplate
from typing import Optional, Any

class TechnicalArchitect(BaseAgent):
    def __init__(self, llm: Optional[Any] = None):
        super().__init__(
            name="Technical Architect",
            role="Technical Architecture",
            tools=["api_designer", "db_schema_generator", "system_architect"],
            llm=llm
        )
        self.prompt_template = PromptTemplate(
            input_variables=["task", "context"],
            template="""
            You are a Technical Architect specializing in:
            - Distributed systems design
            - API architecture (REST, GraphQL)
            - Database optimization
            - Cloud infrastructure (AWS, GCP, Azure)
            - Microservices
            - Security architecture
            - Performance optimization

            For {task}, analyze and provide:
            1. System architecture with scalability focus
            2. API specifications and documentation
            3. Database schema and data flow
            4. Infrastructure requirements
            5. Security measures
            6. Performance optimization strategy

            Context: {context}

            Include:
            - Architecture diagrams requirements
            - API endpoints specification
            - Data models
            - Security protocols
            - Scalability considerations
            """
        )
        
    def _execute_task(self, context):
        return super()._execute_task(context)