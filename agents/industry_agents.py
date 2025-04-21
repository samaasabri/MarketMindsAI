from agents.base_agent import BaseAgent
from models.mistral_model import get_llm
from langchain_core.prompts import ChatPromptTemplate
from utils.web_scraper import scrape_web
from utils.json_utils import extract_json_from_llm_output

def load_prompt(filename):
    """
    Load a prompt template from a file.

    Args:
        filename (str): The name of the prompt file to load.

    Returns:
        ChatPromptTemplate: A Langchain prompt template object.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
        IOError: If there is an issue reading the prompt file.
    """
    try:
        with open(f"prompts/{filename}", "r") as f:
            return ChatPromptTemplate.from_template(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"The prompt file {filename} was not found.")
    except IOError as e:
        raise IOError(f"An error occurred while reading the prompt file {filename}: {e}")

class ResearchAgent(BaseAgent):
    """
    Research Agent class to gather and process web data.

    This class is responsible for scraping the web for information based on a given query.
    It then delegates the work to the base agent for further processing.

    Attributes:
        model (LLM): The language model used for processing the data.
        prompt (ChatPromptTemplate): The prompt template used to process the input data.
    """
    def __init__(self, model):
        """
        Initializes the ResearchAgent with the provided model and loads the research prompt.

        Args:
            model (LLM): The language model used by the agent.
        """
        prompt = load_prompt("research_prompt.txt")
        super().__init__(model, prompt)

    def run(self, query):
        """
        Executes the research task by scraping the web based on the query and processing the data.

        Args:
            query (str): The high-level query for which to gather data.

        Returns:
            dict: The processed research data returned by the base agent.

        Raises:
            Exception: If there is an issue with web scraping or processing the data.
        """
        try:
            web_content = scrape_web(query)
            return super().run({"query": query, "web_content": web_content})
        except Exception as e:
            raise Exception(f"Error during the research task: {e}")

class AnalysisAgent(BaseAgent):
    """
    Analysis Agent class to analyze the research data.

    This class processes the data gathered by the ResearchAgent to provide insights.
    """
    def __init__(self, model):
        """
        Initializes the AnalysisAgent with the provided model and loads the analysis prompt.

        Args:
            model (LLM): The language model used by the agent.
        """
        prompt = load_prompt("analysis_prompt.txt")
        super().__init__(model, prompt)

class StrategyAgent(BaseAgent):
    """
    Strategy Agent class to generate strategic recommendations based on the analysis data.

    This class uses the model to create strategic actions based on the analysis output.
    """
    def __init__(self, model):
        """
        Initializes the StrategyAgent with the provided model and loads the strategy prompt.

        Args:
            model (LLM): The language model used by the agent.
        """
        prompt = load_prompt("strategy_prompt.txt")
        super().__init__(model, prompt)

class WriterAgent(BaseAgent):
    """
    Writer Agent class to generate the final report based on research, analysis, and strategy data.

    This class is responsible for structuring the final report that combines the outputs from other agents.
    """
    def __init__(self, model):
        """
        Initializes the WriterAgent with the provided model and loads the writing prompt.

        Args:
            model (LLM): The language model used by the agent.
        """
        prompt = load_prompt("writer_prompt.txt")
        super().__init__(model, prompt)

class VisualizationAgent(BaseAgent):
    """
    Visualization Agent class to process and visualize the research data.

    This class uses the model to produce visualizations based on the research output.
    """
    def __init__(self, model):
        """
        Initializes the VisualizationAgent with the provided model and loads the visualization prompt.

        Args:
            model (LLM): The language model used by the agent.
        """
        prompt = load_prompt("visualization_prompt.txt")
        super().__init__(model, prompt)

    def run(self, research_data):
        """
        Generates visualizations based on the research data.

        Args:
            research_data (dict): The data from the research agent to visualize.

        Returns:
            dict: A JSON object containing the visualization data.

        Raises:
            Exception: If there is an error during the visualization generation.
        """
        try:
            response = super().run({"research_data": research_data})
            return extract_json_from_llm_output(response)
        except Exception as e:
            raise Exception(f"Error during the visualization generation: {e}")

class IndustryReportOrchestrator:
    """
    Orchestrator for managing the entire process of generating the intelligence report.

    This class coordinates the work of all agents to create a comprehensive industry report based on the query.
    """
    def __init__(self):
        """
        Initializes the orchestrator by creating the necessary agents with the provided model.
        """
        try:
            llm = get_llm()
            self.research_agent = ResearchAgent(llm)
            self.analysis_agent = AnalysisAgent(llm)
            self.strategy_agent = StrategyAgent(llm)
            self.writer_agent = WriterAgent(llm)
            self.visualization_agent = VisualizationAgent(llm)
        except Exception as e:
            raise Exception(f"Error during IndustryReportOrchestrator initialization: {e}")

    def run(self, query):
        """
        Executes the entire workflow for generating a comprehensive industry report.

        Args:
            query (str): The high-level query for generating the report.

        Returns:
            tuple: A tuple containing the final report and visualization output.

        Raises:
            Exception: If there is an issue during any part of the report generation process.
        """
        try:
            research_output = self.research_agent.run(query)
            analysis_output = self.analysis_agent.run({"research_data": research_output})
            visualization_output = self.visualization_agent.run(research_output)
            strategy_output = self.strategy_agent.run({"analysis_data": analysis_output})
            final_report = self.writer_agent.run({
                "research_data": research_output,
                "analysis_data": analysis_output,
                "strategy_data": strategy_output
            })
            return final_report, visualization_output
        except Exception as e:
            raise Exception(f"Error during the report generation process: {e}")
