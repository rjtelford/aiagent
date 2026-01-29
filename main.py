import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import prompts
from Functions.call_function import available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Gemini API Key is blank")
    
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AIAgent")
    parser.add_argument("user_prompt", type=str, help="User Prompt: What do you want?")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=prompts.system_prompt)        
        )
    
    if response.usage_metadata is None:
        raise RuntimeError("Usage Metadata is None")
    elif args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls is not None:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
