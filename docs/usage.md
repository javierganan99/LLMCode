# 🖥️ Usage

LLMCode can be accessed through both the Command-Line Interface (CLI) and Python code. To use the GPT models supported and used by default you should have an OpenAI API Key that you can get [here](https://platform.openai.com/docs/guides/gpt). To use other LLMs to get completions, create your own 'get_completion' function (see [CUSTOM COMPLETIONS](customization.md#custom-completions) section).

First, you need to export your API key:

```ssh
export OPENAI_API_KEY=<YOUR_API_KEY>
```

## CLI

To generate documentation for your code, use the following command:

```ssh
docu <path/to/your/code> [--options]
```

Replace `path/to/your/code` with the path to your folder or script.

The supported CLI options are:

- **--exclude** (optional): Specify files or folders to exclude from documentation. If `path/to/your/code` is a directory, LLMCode will automatically exclude submodules in a git project. If not provided, only git submodules will be excluded.

- **--languages** (optional): Specify the programming languages used in your scripts for documentation. If `path/to/your/code` is a directory, LLMCode will document scripts in the detected language (if supported). Defaults to python.

- **--elements2doc** (optional): Specify the names of elements (functions and/or classes) you want to document. Other elements will not be documented. Defaults to None, which means documenting all elements.

- **--overwrite** (optional): Decide whether to overwrite existing documentation for elements. Defaults to False.

The `path/to/your/code` argument can be the path of a folder or a file. If it is a folder, LLMCode will find all scripts in the provided **--languages** (if supported) and document their elements. If it is a file, it will document all the elements in that file (or those specified in **--elements2doc**).

> By default, LLMCode will overwrite your code at its original location after completing the documentation process. It stores the files in a temporary directory while documenting them. If the process is canceled during execution, the documentation will be lost. If you want to save the documented code in a different location, please refer to the [CUSTOMIZATON](customization.md) section for instructions.

For example, you can document the LLMCode project with the following commands, excluding the scripts in the tests folder and the entrypoint.py script:

```ssh
cd <path/to/LLMCode>
docu . --exclude tests entrypoint.py
```

## Python

LLMCode may also be used directly in a Python environment, and accepts the same arguments as in the CLI example above:

```python
from LLMCode import docu

# Document specified elements of your script
docu(path="path/to/your/script.py", elements2doc=["your_function_name", "your_class_name"], overwrite=True)

# Document your project python scripts
docu(path="path/to/your/project", languages=["python"])
```
