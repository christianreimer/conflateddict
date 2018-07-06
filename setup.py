import setuptools

setuptools.setup(
    name="conflateddict",
    version="0.1.0",
    url="https://github.com/creimer/conflateddict",
    author="Christian Reimer",
    author_email="christian.reimer@gmail.com",
    description="Classes to help conflate streaming data.",
    long_description="This module contains classes to assist with conflating streaming data. This can be used to manage the load on consuming tasks, and is especially useful if the consumers only need the current value and can thus safely discard intermediate updates.>",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)