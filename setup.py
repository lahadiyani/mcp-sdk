from setuptools import setup, find_packages

setup(
    name="mcp-sdk",
    author="Hadiani",
    author_email="lahadiyani@gmail.com",
    version="0.1.0",
    description="Stateless Model Context Protocol SDK",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "anyio==4.12.0",
        "certifi==2025.11.12",
        "h11==0.16.0",
        "httpcore==1.0.9",
        "httpx==0.28.1",
        "idna==3.11",
        "packaging==25.0",
        "pillow==12.1.0",
        "pollinations==4.5.1",
        "typing_extensions==4.15.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-cli=mcp_sdk.shell.cli:main",
            "mcp-http=mcp_sdk.shell.http:main",
            "mcp-stdio=mcp_sdk.shell.stdio:main",
        ],
    },
)
