from setuptools import setup, find_packages

setup(
    name="iam_service",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors", 
        "requests",
        "pyjwt",
        "bcrypt",
        "marshmallow",
        "python-dotenv",
        "flask-migrate",
        "flask_sqlalchemy",
        "psycopg2-binary",
        "pika",
    ],
    python_requires=">=3.8",
) 