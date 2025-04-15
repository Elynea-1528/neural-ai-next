from setuptools import find_packages, setup

setup(
    name="neural-ai-next",
    version="0.1.0",
    author="Neural-AI-Team",
    description="Moduláris, hierarchikus kereskedési rendszer modern gépi tanulási technikákkal",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Private License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "torch",
        "torchvision",
        "torchaudio",
        "lightning",
        "matplotlib",
        "seaborn",
        "pytest",
        "pytest-cov",
    ],
)
