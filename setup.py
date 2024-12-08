from pathlib import Path
from setuptools import setup

# Settings
FILE = Path(__file__).resolve()
PARENT = FILE.parent  # root directory
README = (PARENT / "README.md").read_text(encoding="utf-8")


def parse_requirements(file_path: Path):
    """
Parses a requirements file and returns a list of requirements.

This function reads a given requirements file, processes each line to ignore comments and empty lines, 
and returns a list of requirement strings.

Args:
    file_path (Path): The path to the requirements file.

Returns:
    (list): A list of requirement strings, with comments and empty lines removed.
"""
    requirements = []
    for line in Path(file_path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            requirements.append(line.split("#")[0].strip())  # ignore inline comments

    return requirements


setup(
    name="LLMCode",
    description=("LLMCode for coding using Large Languages Models"),
    author="Francisco Javier Gañán",
    author_email="fjganan14@gmail.com",
    version="0.1",
    packages=["llmcode"]
    + [
        str(x) for x in Path("llmcode").rglob("*/") if x.is_dir() and "__" not in str(x)
    ],
    package_data={"config_files": ["*.yaml"], "prompts": ["*.txt"]},
    include_package_data=True,
    install_requires=parse_requirements(PARENT / "requirements.txt"),
    keywords="deep-learning, Large Language Models, LLM, Programming",
    entry_points={
        "console_scripts": [
            "docu = llmcode.entrypoint:main",
        ],
    },
)
