from setuptools import setup
from pathlib import Path

# Settings
FILE = Path(__file__).resolve()
PARENT = FILE.parent  # root directory
README = (PARENT / "README.md").read_text(encoding="utf-8")


def parse_requirements(file_path: Path):
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
    packages=["LLMCode"]
    + [
        str(x) for x in Path("LLMCode").rglob("*/") if x.is_dir() and "__" not in str(x)
    ],
    package_data={"": ["*.yaml"], "": ["*.txt"]},
    include_package_data=True,
    install_requires=parse_requirements(PARENT / "requirements.txt"),
    keywords="deep-learning, Large Language Models, LLM, Programming",
    entry_points={
        "console_scripts": [
            "docu = LLMCode.entrypoint:main",
        ],
    },
)
