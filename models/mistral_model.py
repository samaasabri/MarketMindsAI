import os
from langchain_mistralai import ChatMistralAI

def get_llm():
    """
    Loads the Mistral LLM model, checking for an existing API key in the environment variables.
    If the key is not found, it prompts the user to enter it.

    Returns:
        ChatMistralAI: An instance of the ChatMistralAI model with the specified settings.

    Raises:
        EnvironmentError: If the MISTRAL_API_KEY is not found and the user does not provide it.
    """
    try:
        # Check if the Mistral API key is already set in the environment
        mistral_key = os.getenv("MISTRAL_API_KEY")

        if not mistral_key:
            # If no key found in the environment, prompt the user for it (only for local dev)
            import getpass
            mistral_key = getpass.getpass("Enter your Mistral API key: ")

            if not mistral_key:
                raise EnvironmentError("MISTRAL_API_KEY not found and no key provided.")

            # Set the provided key as an environment variable (optional, only for local dev)
            os.environ["MISTRAL_API_KEY"] = mistral_key

        # Return an instance of the ChatMistralAI model with the specified configurations
        return ChatMistralAI(
            model="mistral-large-latest",
            temperature=0,  # Set temperature to 0 for deterministic responses
            max_retries=5,  # Allow retries in case of failure
        )

    except Exception as e:
        raise Exception(f"Error initializing the Mistral model: {e}")
