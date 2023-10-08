<div></div>
<img align="left" src="LLMCode/assets/images/logo.png" alt="LLMCode" width="300" height: auto;">

# LLMCode
LLMCode is a tool designed to streamline code documentation using Language Models (LLMs).
  </br>
  </br>
It is a user-friendly utility that harnesses the capabilities of Language Models to automatically generate code documentation. Say goodbye to the time-consuming and often tedious task of writing documentation by hand. With this tool, you can effortlessly self-updating code documentation, and then just review the work of LLMCode.
</br>
</br>

## 📋 Features

- [x] **Seamless Integraton**: LLMCode is a Python package installable via pip, compatible with various code editors, and seamlessly integrates with Git version control system.

- [x] **Customizaton**: Tailor the generated documentation to your needs by creating custom prompts. You can define the documentation format, with separate prompts for functions and classes.

- [x] **Python support**: LLMCode fully supports Python, allowing you to generate docstrings for functions and classes within your Python scripts. Document your entire project, specific scripts, or selected functions, and decide whether or not to overwrite existing documentation. All this can be achieved with straightforward CLI commands or by utilizing the Python library. Check out the [USAGE](#🖥️-usage) section for more details.

- [x] **GPT models**: LLMCode currently supports GPT models, leveraging the OpenAI API for prompt-based completions. However, for users interested in interacting with other Language Models (LLMs), it's easy to create a custom 'get_completion' method. Detailed instructions can be found in the [CUSTOM COMPLETIONS](#custom-completions) section.

## ⚙️ Installation

To install LLMCode you can use pip.

- Just use it.

    ```ssh
    pip install git+https://github.com/javierganan99/LLMCode.git
    ```

- Editable mode (recommended).

    1. Clone the repository.
        ```ssh
        git clone https://github.com/javierganan99/LLMCode.git
        cd LLMCode
        ```

    2. Install the tool using pip.

        Editable mode.

        ```ssh
        pip install -e .
        ```

        For developers. To access the latest features and updates and for contributors.

        ```ssh
        git checkout develop
        pip install -e .
        ```

## 🖥️ Usage

LLMCode can be accessed through both the Command-Line Interface (CLI) and Python code. To use the GPT models supported and used by default you should have an OpenAI API Key that you can get [here](https://platform.openai.com/docs/guides/gpt). To use other LLMs to get completions, create your own 'get_completion' function (see [CUSTOM COMPLETIONS](#custom-completions) section).

First, you need to export your API key:

```ssh
export OPENAI_API_KEY=<YOUR_API_KEY>
```

### CLI

To generate documentation for your code, use the following command:


```ssh
docu <path/to/your/code> [--options]
```

Replace **<path/to/your/code>** with the path to your folder or script.

The supported CLI options are:

- **--exclude** (optional): Specify files or folders to exclude from documentation. If **<path/to/your/code>** is a directory, LLMCode will automatically exclude submodules in a git project. If not provided, only git submodules will be excluded.

- **--languages** (optional): Specify the programming languages used in your scripts for documentation. If **<path/to/your/code>** is a directory, LLMCode will document scripts in the detected language (if supported). Defaults to python.

- **--elements2doc** (optional): Specify the names of elements (functions and/or classes) you want to document. Other elements will not be documented. Defaults to None, which means documenting all elements.

- **--overwrite** (optional): Decide whether to overwrite existing documentation for elements. Defaults to False.

The **<path/to/your/code>** argument can be the path of a folder or a file. If it is a folder, LLMCode will find all scripts in the provided **--languages** (if supported) and document their elements. If it is a file, it will document all the elements in that file (or those specified in **--elements2doc**).

> By default, LLMCode will overwrite your code at its original location after completing the documentation process. It stores the files in a temporary directory while documenting them. If the process is canceled during execution, the documentation will be lost. If you want to save the documented code in a different location, please refer to the [CUSTOMIZE](#customize) section for instructions.

For example, you can document the LLMCode project with the following commands, excluding the scripts in the tests folder and the entrypoint.py script:

```ssh
cd <path/to/LLMCode>
docu . --exclude tests entrypoint.py
```

### Python

LLMCode may also be used directly in a Python environment, and accepts the same arguments as in the CLI example above:

```python
from LLMCode import docu

# Document specified elements of your script
docu(path="path/to/your/script.py", elements2doc=["your_function_name", "your_class_name"], overwrite=True)

# Document your project python scripts
docu(path="path/to/your/project", languages=["python"])
```


## 🛠 Customize

In addition to the CLI and Python-supported options, you can further customize LLMCode by editing the **<path/to/this/repo/LLMCode/cfg/custom_params.py>**  script. Here, you can fine-tune various parameters to suit your specific needs. Further, you can easily customize LLMCode in two ways: creating your custom completion functions and creating your custom prompts.

### Custom Completions

You have the flexibility to create your custom completion functions, even with your own LLMs. To integrate your custom completion function, follow these two steps:

1. Define your 'get_completion' function. You should do so in the **<path/to/this/repo/LLMCode/utils/completion.py>** file. Here's an example of how the 'get_completion_openai' function is defined:

    ```python
    import openai
    import LLMCode.cfg.completion_params as completion_params

    def get_completion_openai(prompt):
        params = {
            key: value
            for key, value in vars(completion_params).items()
            if not key.startswith("__")
        }
        chat_completion = openai.ChatCompletion.create(
            messages=[{"role": "user", "content": prompt}], **params
        )
        return chat_completion.choices[0].message.content
    ```

    Ensure that the function you define takes only a prompt (str) as input and outputs a response (str). The remaining parameters required for the function must be defined in **<path/to/this/repo/LLMCode/cfg/completion_params.py>** and loaded in the **completion.py** script, similar to how it's done for the 'get_completion_openai' function. For naming your function, it's recommended to follow the 'get_completion_XXX' naming convention.

2. Configure the 'get_completion' function you want to use in the **<path/to/this/repo/LLMCode/cfg/completion_params.py>** script.

    ```python
    completion_function = "YOUR_COMPLETION_FUNCTION"
    ```

> If you have a 'get_completion_XXX' function that you believe could benefit others, please consider [contributing](./CONTRIBUTING.md).

### Custom Prompts

You can write your own prompts to customize the documentation process. To do so, follow these steps:

1. It is recommended to define them in the **<path/to/this/repo/LLMCode/prompts/YOUR_USED_PROGRAMMING_LANGUAGE>** folder. These prompts should be saved as *.txt* files. For example, Python prompts can be defined in the **<path/to/this/repo/LLMCode/prompts/python>** folder, with separate prompts for functions and classes. Here's an example of the 'documentFunction.txt' prompt used for documenting Python functions in the Google format:

    ```txt
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

2. Specify the paths of your custom prompts in the  **<path/to/this/repo/LLMCode/cfg/custom_params.py>** file. If you have defined prompts in the **<path/to/this/repo/LLMCode/prompts/YOUR_USED_PROGRAMMING_LANGUAGE>** folder, update the configuration like this:

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

> If you discover prompts that work well with a specific LLM, please consider [contributing](./CONTRIBUTING.md).

## 📬 Contact

Francisco Javier Gañán - fjganan14@gmail.com
