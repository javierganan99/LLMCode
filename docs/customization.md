# 🛠 Customization

In addition to the CLI and Python-supported options, you can further customize LLMCode by editing the `path/to/this/repo/LLMCode/cfg/custom_params.py` script. Here, you can fine-tune various parameters to suit your specific needs. Further, you can easily customize LLMCode in two ways: creating your custom completion functions and creating your custom prompts.

## Custom Completions

You have the flexibility to create your custom completion functions, even with your own LLMs. To integrate your custom completion function, follow these two steps:

1. Define your `get_completion` function. You should do so in the `path/to/this/repo/LLMCode/utils/completion.py` file. Here's an example of how the `get_completion_openai` function is defined:

```python
import openai
import LLMCode.cfg.completion_params as completion_params

def get_completion_openai(prompt):
    params = {
        key: value
        for key, value in vars(completion_params).items()
        if not key.startswith("__")
    }
    return openai.ChatCompletion.create(
        messages=[{"role": "user", "content": prompt}], **params
    ).choices[0].message.content
```

Ensure that the function you define takes only a prompt (str) as input and outputs a response (str). The remaining parameters required for the function must be defined in `path/to/this/repo/LLMCode/cfg/completion_params.py` and loaded in the `completion.py` script, similar to how it's done for the 'get_completion_openai' function. For naming your function, it's recommended to follow the `get_completion_XXX` naming convention. If the function is capable of generating any exceptions, they should be included in the return statement. This is crucial to ensure that the upstream functions handle the exceptions appropriately.

2. Configure the 'get_completion' function you want to use in the `path/to/this/repo/LLMCode/cfg/completion_params.py` script.

   ```python
   completion_function = "YOUR_COMPLETION_FUNCTION"
   ```

> If you have a 'get_completion_XXX' function that you believe could benefit others, please consider [contributing](https://github.com/javierganan99/LLMCode/blob/main/CONTRIBUTING.md).

## Custom Prompts

You can write your own prompts to customize the documentation process. To do so, follow these steps:

1. It is recommended to define them in the `path/to/this/repo/LLMCode/prompts/YOUR_USED_PROGRAMMING_LANGUAGE` folder. These prompts should be saved as _.txt_ files. For example, Python prompts can be defined in the `path/to/this/repo/LLMCode/prompts/python` folder, with separate prompts for functions and classes. Here's an example of the 'documentFunction.txt' prompt used for documenting Python functions in the Google format:

```
Please, provide the docstring for the following FUNCTION in the following DOCSTRING FORMAT (that is the Google format for Python docstrings). If the FUNCTION already has a docstring, check that it is correct and change what do you think it is convenient.
If the DOCSTRING FORMAT is not the provided one, change the format of the docstring.

FUNCTION:
    !<QUERY COMPLETION>!

DOCSTRING FORMAT:
    """
    Summary of the function.

    More extensive description that allows for its complete understanding.

    Args:
        param1 (type1 | type2): Description of param1.
        param2 (type, optional): Description of param2.
        param3 (type): Description of param3 (default is default_paramerer_value).
        ...

    Returns:
        type: Description of the return param.
    """

I want you to generate as output only the docstring (in the specified format) and between triple quotes, without more text.
The output is intended to be copied directly to a code script.

```

Make sure to include the **\!\<QUERY COMPLETION\>\!** placeholder where you want your element (function or class) to be located, as LLMCode will replace it.

2. Specify the paths of your custom prompts in the `path/to/this/repo/LLMCode/cfg/custom_params.py` file. If you have defined prompts in the `path/to/this/repo/LLMCode/prompts/YOUR_USED_PROGRAMMING_LANGUAGE` folder, update the configuration like this:

```python
document_prompts = {  # Queries for the model to document function and classes
    "YOUR_USED_PROGRAMMING_LANGUAGE": {
        "function": Path(__file__).parent
        / f"..{os.path.sep}prompts{os.path.sep}YOUR_USED_PROGRAMMING_LANGUAGE{os.path.sep}YOUR_PROMPT_FOR_FUNTIONS.txt",
        "class": Path(__file__).parent
        / f"..{os.path.sep}prompts{os.path.sep}YOUR_USED_PROGRAMMING_LANGUAGE{os.path.sep}YOUR_PROMPT_FOR_CLASSES.txt",
    }
}
```

> If you discover prompts that work well with a specific LLM, please consider [contributing](https://github.com/javierganan99/LLMCode/blob/main/CONTRIBUTING.md).
