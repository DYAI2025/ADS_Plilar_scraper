#!/usr/bin/env python3
from setuptools import setup, find_packages
from pathlib import Path

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

readme_path = Path(__file__).parent / "Files" / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="ads-pillar-scraper",
    version="1.0.0",
    description="Automated Pillar-Page generation tool with AdSense monetization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DYAI",
    author_email="ben.poersch@dyai.app",
    url="https://github.com/DYAI2025/ADS_Plilar_scraper",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ads-pillar-gui=Files.gui_app:main",
            "ads-pillar-quick=Files.quick_start:main",
            "ads-pillar-niche=Files.niche_research:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
