from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentic-patterns",
    version="0.1.0",
    author="Balaram",
    author_email="bpan575@aucklanduni.ac.nz",
    description="A standardized library for AI agent design patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/balrm/agentic-patterns",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords="ai, agents, patterns, llm, prompt-engineering",
    project_urls={
        "Bug Reports": "https://github.com/balrm/agentic-patterns/issues",
"Source": "https://github.com/balrm/agentic-patterns",
"Documentation": "https://github.com/balrm/agentic-patterns#readme",
        "ORCID": "https://orcid.org/0000-0001-5977-8392",
        "GitHub": "https://github.com/balrm",
    },
) 