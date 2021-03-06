from setuptools import find_packages, setup


def install_requires():
    with open("requirements.txt") as f:
        return [r.strip() for r in f.readlines()]


setup(
    name="Macrome",
    description="Discord macro bot",
    author="Princess Lana",
    author_email="ianagbip1oti@gmail.com",
    url="https://github.com/ianagbip1oti/macrome",
    packages=find_packages(),
    use_scm_version=True,
    install_requires=install_requires(),
    setup_requires=["setuptools-scm==3.3.3"],
)
