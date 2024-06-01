# useful helper functions for gemini function calls: 

# Helper function to extract one or more function calls from a Gemini Function Call response
def extract_function_calls(response: GenerationResponse) -> List[Dict]:
    function_calls = []
    if response.candidates[0].function_calls:
        for function_call in response.candidates[0].function_calls:
            function_call_dict = {function_call.name: {}}
            for key, value in function_call.args.items():
                function_call_dict[function_call.name][key] = value
            function_calls.append(function_call_dict)
    return function_calls

def extract_function_call_names(response: GenerationResponse) -> List[str]:
    pass