from .base_agent import BaseAgent
from typing import Dict, Optional, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
import logging

class ProjectManager(BaseAgent):
    def __init__(self, llm: Optional[BaseLanguageModel] = None):
        """
        Initialize the ProjectManager with a specific role and optional LLM.
        
        :param llm: Language model chain for the agent
        """
        super().__init__(name="Project Manager", role="Manage the whole project", llm=llm)
        # Update template for better synthesis
        self.prompt_template = PromptTemplate(
            input_variables=["task", "context"],
            template="""
            You are a seasoned Project Manager synthesizing insights from multiple experts.
            
            Project Brief: {task}
            
            Expert Insights: {context}
            
            Provide a comprehensive, well-structured report covering:
            1. Executive Summary
            2. Strategic Overview
            3. Technical Implementation Plan
            4. User Experience & Design
            5. Growth & Marketing Strategy
            6. DevOps & Infrastructure
            7. Risk Assessment & Mitigation
            8. Timeline & Milestones
            9. Resource Requirements
            10. Next Steps & Recommendations
            
            Make sure to integrate insights from all experts into a cohesive narrative.
            """
        )
        
        self.followup_template = PromptTemplate(
            input_variables=["question", "brief", "insights"],
            template="""
            Based on the project analysis:
            
            Original Brief: {brief}
            Expert Insights: {insights}
            
            Answer this follow-up question: {question}
            
            Provide a clear, specific answer drawing from the available information.
            """
        )
        
        self.planning_template = PromptTemplate(
            input_variables=["brief"],
            template="""
            As a Project Manager, create specific tasks for each specialist based on this brief:

            Brief: {brief}

            For each specialist, define their focus areas and specific tasks.
            Format your response in a way that's easy to parse, using --- as separators:

            STRATEGIC_LEAD
            ---
            [Write your strategic analysis and planning tasks here]
            ---

            GROWTH_STRATEGIST
            ---
            [Write your growth and marketing tasks here]
            ---

            UX_DESIGNER
            ---
            [Write your UX/UI design tasks here]
            ---

            TECH_ARCHITECT
            ---
            [Write your technical architecture tasks here]
            ---

            DEVOPS_SPECIALIST
            ---
            [Write your infrastructure and deployment tasks here]
            ---
            """
        )
        
        self.synthesis_template = PromptTemplate(
            input_variables=["brief", "insights"],
            template="""
            As a Project Manager, synthesize all specialist insights into a cohesive project plan.
            
            Original Brief: {brief}
            
            Specialist Insights: {insights}
            
            Provide a comprehensive project analysis covering:
            1. Executive Summary (High-level overview and key recommendations)
            2. Project Scope & Objectives
            3. Implementation Strategy
    - Technical Architecture
    - User Experience
    - Growth & Marketing
    - Infrastructure & DevOps
            4. Risk Assessment & Mitigation
            5. Timeline & Milestones
            6. Resource Requirements & Budget Estimates
            7. Success Metrics & KPIs
            8. Next Steps & Recommendations
            
            Focus on providing actionable insights and clear direction.
            """
        )
    
    def manage_project(self, brief: str, agent_insights: Dict[str, str]) -> str:
        """
        Manage the project by synthesizing insights from all agents and presenting the final answer.
        
        :param brief: Project brief
        :param agent_insights: Insights from all agents
        :return: Final synthesized answer
        """
        try:
            # Format context properly for chain execution
            return self._execute_task({
                'task': brief,
                'context': str(agent_insights)  # Convert insights to string
            })
        except Exception as e:
            logging.error(f"Project management failed: {e}")
            return f"Error in project management: {str(e)}"

    def interact_with_user(self, user_input: str) -> str:
        """
        Interact with the user to provide updates or gather more information.
        
        :param user_input: Input from the user
        :return: Response to the user
        """
        try:
            context = {
                'user_input': user_input,
                'role': self.role,
                'memory': self.memory.load_memory_variables({})
            }
            return self._execute_task(context)
        except Exception as e:
            logging.error(f"Interaction with user failed: {e}")
            raise

    def _execute_task(self, context: Dict) -> str:
        return super()._execute_task(context)
    
    def answer_followup(self, context: Dict) -> str:
        """Handle follow-up questions about the project"""
        try:
            # Updated: Use the new chain pattern
            chain = self.followup_template | self.llm
            response = chain.invoke({
                "question": context['question'],
                "brief": context['brief'],
                "insights": str(context['insights'])
            })
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logging.error(f"Follow-up handling failed: {e}")
            return f"Error answering follow-up: {str(e)}"
    
    def create_project_plan(self, brief: str) -> Dict[str, str]:
        """Create specific tasks for each specialist based on the brief."""
        try:
            chain = self.planning_template | self.llm | self.output_parser
            response = chain.invoke({"brief": brief})
            
            plan = self._parse_plan(response)
            return plan if plan else self._get_default_tasks()
            
        except Exception as e:
            logging.error(f"Project planning failed: {e}")
            return self._get_default_tasks()

    def _parse_plan(self, content: str) -> Dict[str, str]:
        try:
            plan = {}
            sections = content.split('---')
            current_role = None
            
            for section in sections:
                section = section.strip()
                if any(role in section.upper() for role in ['STRATEGIC_LEAD', 'GROWTH_STRATEGIST', 'UX_DESIGNER', 'TECH_ARCHITECT', 'DEVOPS_SPECIALIST']):
                    current_role = section.lower().replace('_', '')
                elif current_role and section:
                    plan[current_role] = section.strip()
            
            return plan
        except:
            return {}

    def _get_default_tasks(self) -> Dict[str, str]:
        return {
            'strategic_lead': 'Analyze market opportunity and competitive landscape',
            'growth_strategist': 'Develop growth strategy and marketing plan',
            'ux_designer': 'Design user experience and interface',
            'tech_architect': 'Design technical architecture and systems',
            'devops_specialist': 'Plan infrastructure and deployment'
        }
    
    def synthesize_insights(self, brief: str, agent_insights: Dict[str, str]) -> str:
        """Create final synthesis of all agent insights."""
        try:
            chain = self.synthesis_template | self.llm
            response = chain.invoke({
                "brief": brief,
                "insights": str(agent_insights)
            })
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logging.error(f"Synthesis failed: {e}")
            return f"Error in synthesis: {str(e)}"