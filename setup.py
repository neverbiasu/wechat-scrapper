from setuptools import setup, find_packages

setup(
    name="wechat-scrapper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml",
        "wechatarticles",
        "black",
        "pre-commit",
        "pytest",
    ],
    entry_points={
        "console_scripts": ["wechat-scrapper=wechat_scrapper.cli:main"],
    },
)
