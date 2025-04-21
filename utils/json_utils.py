import re
import json

def extract_json_from_llm_output(llm_output):
    """
    Extracts a JSON object from the LLM output enclosed in ```json``` code blocks.

    Parameters:
    - llm_output (str): The string output from the LLM, which may contain a JSON block.

    Returns:
    - dict or None: The parsed JSON object if found and successfully decoded, otherwise None.
    
    Logs:
    - Error messages if no JSON is found or if there is an issue during JSON decoding.
    """
    # Regular expression to find the JSON part in the LLM output
    match = re.search(r'```json\s*(\{.*?\})\s*```', llm_output, re.DOTALL)
    
    if match:
        try:
            # Extract the JSON string and parse it
            json_str = match.group(1)
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Error handling for invalid JSON
            print(f"Error decoding JSON: {e}")  # Optionally log this message
            return None
    else:
        # Log if no JSON block is found
        print("No JSON block found in the LLM output.")
        return None
