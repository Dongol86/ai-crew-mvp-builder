from langchain_ollama import OllamaLLM
from langchain.chains import SequentialChain
from utils.document_processor import DocumentProcessor
from agents import *
import yaml
import logging
from typing import Dict, List, Optional
from agents.strategic_lead import StrategicLead
from agents.growth_strategist import GrowthStrategist 
from agents.ux_designer import UXDesigner
from agents.tech_architect import TechnicalArchitect
from agents.devops_specialist import DevOpsSpecialist

class AICrew:
   def __init__(self):
       self.llm = OllamaLLM(model="llama3.2")
       self.doc_processor = DocumentProcessor()
       self.load_config()
       self.initialize_agents()
       logging.basicConfig(level=logging.INFO)
       
   def load_config(self):
       try:
           with open('config/config.yaml', 'r') as file:
               self.config = yaml.safe_load(file)
       except Exception as e:
           logging.error(f"Config load failed: {e}")
           raise
           
   def initialize_agents(self):
       self.agents = {
            'strategic_lead': StrategicLead(llm=self.llm),
            'growth_strategist': GrowthStrategist(llm=self.llm),
            'ux_designer': UXDesigner(llm=self.llm),
            'tech_architect': TechnicalArchitect(llm=self.llm),
            'devops_specialist': DevOpsSpecialist(llm=self.llm)
       }

   def process_project(self, project_brief: str, documents: Optional[List[str]] = None) -> Dict:
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
           raise

   def _process_with_agents(self, brief: str) -> Dict:
       project_context = {}
       for agent_name, agent in self.agents.items():
           try:
               logging.info(f"Processing with {agent_name}")
               result = agent.process_task(brief)
               project_context[agent_name] = result
               brief = self.enrich_brief(brief, project_context)
           except Exception as e:
               logging.error(f"Agent {agent_name} failed: {e}")
               project_context[agent_name] = f"Failed: {str(e)}"
       return project_context

   def enrich_brief(self, brief: str, context: Dict) -> str:
       return f"""
       Original Brief: {brief}
       Current Context: {context}
       Additional Documentation: {bool(context)}
       """

if __name__ == "__main__":
   crew = AICrew()