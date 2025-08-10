import os
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from src.laptop_repair.tools.custom_tool import SystemCommandTool

def load_yaml(file_path: str) -> dict:
    """Helper function to load a YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

class LaptopRepairCrew:
    def __init__(self, problem_description: str):
        self.problem_description = problem_description
        # Path to the config files (assuming they are in a 'config' subdirectory)
        self.config_path = os.path.join(os.path.dirname(__file__), 'config')

        # Retrieve API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please provide the API key.")
            
        # Initialize the Gemini LLM with enhanced settings for better batch script generation
        self.llm = LLM(model="gemini/gemini-1.5-flash-latest", api_key = api_key)

    def run(self):
        """
        Initializes and runs the crew with configurations loaded from YAML files.
        Returns a comprehensive diagnosis and batch script for fixing the system issue.
        """
        # Load agent and task configurations from YAML
        agents_config = load_yaml(os.path.join(self.config_path, 'agents.yaml'))
        tasks_config = load_yaml(os.path.join(self.config_path, 'tasks.yaml'))
 
        # Instantiate the enhanced system diagnostic tool
        system_tool = SystemCommandTool()

        # --- Create the Lead Diagnostician Agent ---
        lead_diagnostician = Agent(
            **agents_config['lead_diagnostician_agent'],
            tools=[system_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        # --- Create the System Analysis Task ---
        system_analysis_task = Task(
            **tasks_config['system_analysis_task'],
            agent=lead_diagnostician,
        )

        # --- Assemble the Crew ---
        crew = Crew(
            agents=[lead_diagnostician],
            tasks=[system_analysis_task],
            process=Process.sequential,
            verbose=True
        )

        print("🔧 Laptop Repair Crew: Starting comprehensive system diagnosis...")
        print(f"📋 Problem to investigate: {self.problem_description}")
        
        try:
            # Execute the crew with the problem description
            result = crew.kickoff(inputs={'problem_description': self.problem_description})
            
            print("✅ Laptop Repair Crew: Diagnosis and batch script generation complete.")
            
            # Ensure the result is properly formatted
            if hasattr(result, 'raw'):
                return str(result.raw)
            else:
                return str(result)
                
        except Exception as e:
            print(f"❌ Error during crew execution: {str(e)}")
            # Return a fallback diagnostic report
            return f"""
**Problem Summary:** {self.problem_description}

**Diagnostic Results:** An error occurred during the automated diagnosis process.

**Root Cause Analysis:** Unable to complete automated diagnosis due to: {str(e)}

**Recommended Action:** Please try the following manual steps:
1. Run Windows System File Checker
2. Check for Windows Updates
3. Restart your computer
4. Contact technical support if issues persist

**Manual Diagnostic Commands to Try:**
```
systeminfo
sfc /scannow
chkdsk C: /f
```

Note: The automated batch script generation failed. Please run these commands manually in an Administrator Command Prompt.
"""

    def get_system_info(self):
        """Helper method to get basic system information for debugging."""
        try:
            system_tool = SystemCommandTool()
            return system_tool._run("systeminfo")
        except Exception as e:
            return f"Unable to retrieve system information: {str(e)}"