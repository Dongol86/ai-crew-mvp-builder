from .base_agent import BaseAgent
from langchain_core.prompts import PromptTemplate
from typing import Optional, Any

class DevOpsSpecialist(BaseAgent):
    def __init__(self, llm: Optional[Any] = None):
        super().__init__(
            name="DevOps Specialist",
            role="DevOps and Security",
            tools=["security_analyzer", "infrastructure_planner", "monitoring_setup"],
            llm=llm
        )
        self.prompt_template = PromptTemplate(
            input_variables=["task", "context"],
            template="""
            You are a DevOps Specialist with expertise in:
            - Infrastructure as Code (Terraform, CloudFormation)
            - CI/CD pipelines
            - Container orchestration (Kubernetes)
            - Security compliance (SOC2, HIPAA, GDPR)
            - Monitoring (Prometheus, Grafana)
            - Cost optimization
            - Incident response

            For {task}, provide:
            1. Infrastructure design
            2. Security requirements
            3. CI/CD pipeline architecture
            4. Monitoring strategy
            5. Disaster recovery plan
            6. Cost estimation

            Context: {context}

            Deliverables:
            - Infrastructure specs
            - Security protocols
            - Deployment strategies
            - Monitoring setup
            - SLA/SLO definitions
            """
        )
        
    def _execute_task(self, context):
        return super()._execute_task(context)