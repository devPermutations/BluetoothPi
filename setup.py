from setuptools import setup, find_packages

setup(
    name="bluetooth_scanner",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "dbus-python>=1.3.2",
        "pydbus>=0.6.0",
        "python-dotenv>=1.0.0",
        "SQLAlchemy>=2.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "bluetooth-scanner=bluetooth_scanner.__main__:main",
            "bluetooth-visualizer=bluetooth_scanner.visualizer:main",
        ],
    },
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Bluetooth device scanner for Raspberry Pi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bluetooth-scanner",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 