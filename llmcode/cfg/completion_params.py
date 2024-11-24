"""
This module defines the parameters for the completion function used in the application.
It specifies the completion function to be used, the model, and the maximum number of tokens.

Attributes:
    completion_function (str): The name of the completion function to use.
    model (str): The model identifier for the completion function.
    max_tokens (int): The maximum number of tokens allowed in the completion.

Author: Francisco Javier Gañán
License File: https://github.com/javierganan99/LLMCode/blob/main/LICENSE
"""

completion_function = "get_completion_openai"
# See https://platform.openai.com/docs/api-reference/chat/create
#         for a list of valid parameters.
model = "gpt-4o-mini"
max_tokens = 600
