from utils.logger import get_logger

logger = get_logger(__name__)

class BaseAgent:
    """
    A base agent that connects a prompt template with a language model
    to form an executable processing chain.

    Attributes:
        chain: A composed chain of the prompt template and model.
    """

    def __init__(self, model, prompt_template):
        """
        Initializes the BaseAgent with a model and prompt template.

        Args:
            model: The language model to be used.
            prompt_template: A formatted prompt template chain component.
        """
        self.chain = prompt_template | model
        logger.info("BaseAgent initialized with model and prompt template.")

    def run(self, input_data):
        """
        Executes the processing chain with the given input data.

        Args:
            input_data (dict): A dictionary of input variables for the prompt.

        Returns:
            str: The generated content from the model's response.
        """
        try:
            logger.debug(f"BaseAgent running with input: {input_data}")
            result = self.chain.invoke(input_data).content
            logger.debug(f"BaseAgent result: {result}")
            return result
        except Exception as e:
            logger.error("Error during BaseAgent chain invocation", exc_info=True)
            return "An error occurred during processing."
