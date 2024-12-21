import yaml
import logging
from typing import Dict, List, Optional
from langchain_ollama import OllamaLLM
from langchain_core.language_models.base import BaseLanguageModel
from utils.document_processor import DocumentProcessor
from agents.strategic_lead import StrategicLead
from agents.growth_strategist import GrowthStrategist 
from agents.ux_designer import UXDesigner
from agents.tech_architect import TechnicalArchitect
from agents.devops_specialist import DevOpsSpecialist
from agents.manager_agent import ProjectManager
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO)

class AICrew:
    def __init__(self):
        # Updated: Configure LLM with specific parameters
        self.llm = OllamaLLM(
            model="llama3.2",
            temperature=0.7,
            streaming=True,
            model_kwargs={"top_k": 50}
        )
        self.doc_processor = DocumentProcessor()
        self.load_config()
        self.initialize_agents()
        # Add memory to store complete project context
        self.project_memory = {}
       
    def load_config(self):
        """Load configuration from a YAML file."""
        try:
            with open('config/config.yaml', 'r') as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError as e:
            logging.error(f"Config file not found: {e}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing config file: {e}")
            raise
        except Exception as e:
            logging.error(f"Config load failed: {e}")
            raise
           
    def initialize_agents(self):
        """Initialize all agents."""
        self.manager = ProjectManager(llm=self.llm)
        self.agents = {
            'strategic_lead': StrategicLead(llm=self.llm),
            'growth_strategist': GrowthStrategist(llm=self.llm),
            'ux_designer': UXDesigner(llm=self.llm),
            'tech_architect': TechnicalArchitect(llm=self.llm),
            'devops_specialist': DevOpsSpecialist(llm=self.llm)
        }

    def process_project(self, project_brief: str, documents: Optional[List[str]] = None) -> Dict:
        """Process a project brief with optional documents."""
        try:
            doc_context = {}
            if documents:
                for doc_path in documents:
                    doc_content = self.doc_processor.process_file(doc_path)
                    doc_context[doc_path] = doc_content
           
            enriched_brief = self.enrich_brief(project_brief, doc_context)
            return self._process_with_agents(enriched_brief)
           
        except Exception as e:
            logging.error(f"Project processing failed: {e}")
            return {"error": str(e)}  # Return error in results format

    def _process_with_agents(self, brief: str) -> Dict:
        """Process the brief with project manager coordination."""
        try:
            # Get initial plan from PM
            initial_plan = self.manager.create_project_plan(brief)
            logging.info(f"Project plan created successfully")
            
            # Process agents based on PM's direction
            agent_insights = {}
            with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
                futures = {
                    executor.submit(
                        agent.process_task, 
                        {
                            'task': initial_plan.get(agent_name, ''),
                            'context': brief
                        }
                    ): agent_name 
                    for agent_name, agent in self.agents.items()
                }
                
                for future in as_completed(futures, timeout=120):
                    agent_name = futures[future]
                    try:
                        result = future.result()
                        agent_insights[agent_name] = result
                        logging.info(f"Agent {agent_name} completed task")
                    except Exception as e:
                        logging.error(f"Agent {agent_name} failed: {e}")
                        agent_insights[agent_name] = str(e)
            
            # Store context for follow-up questions
            self.project_memory.update({
                'brief': brief,
                'insights': agent_insights
            })
            
            # Get final synthesis from PM
            synthesis = self.manager.synthesize_insights(brief, agent_insights)
            return {"synthesis": synthesis}
            
        except Exception as e:
            logging.error(f"Project processing failed: {e}")
            return {"error": f"Analysis failed: {str(e)}"}

    def enrich_brief(self, brief: str, context: Dict) -> str:
        return f"""
        Original Brief: {brief}
        Current Context: {context}
        Additional Documentation: {bool(context)}
        """

    def ask_followup(self, question: str) -> str:
        """Handle follow-up questions about the project"""
        if not self.project_memory:
            return "Please analyze a project first before asking follow-up questions."
            
        context = {
            'question': question,
            'brief': self.project_memory['brief'],
            'insights': self.project_memory['insights']
        }
        return self.manager.answer_followup(context)

if __name__ == "__main__":
    crew = AICrew()