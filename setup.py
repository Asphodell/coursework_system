from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
      long_description = fh.read()

setup(name='floatingparser',
      version='1.0.2.3',
      install_requires = ['numpy',
                          'pandas',
                          'plotly',
                          'streamlit'
                          ],
      author='Vladislav "Asphodel" Shabalin',
      description='Parser for floating server logs',
      long_description=long_description,  
      long_description_content_type='text/markdown',
      packages=['floatingparser'],
      author_email='vladislaus.shabalin@yandex.ru',
      url="https://github.com/Asphodell/coursework_system",
      zip_safe=False)