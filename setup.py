from setuptools import setup, find_packages

setup(
    name="st3215-servo",        # package name (pip name)
    version="0.1.0",
    description="Python library for ST3215 bus servo control",
    author="Saksham Agarwal",
    packages=find_packages(),  # automatically finds servo_control
)
