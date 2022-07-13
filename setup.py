from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Planilhas',
    url='https://github.com/rogeriomoreirajr/Planilhas',
    author='Rogério Moreira Jr.',
    author_email='rogeriomoreirajr@gmail.com',
    # Needed to actually package something
    packages=['planilhas'],
    # Needed for dependencies
    install_requires=['gspread', 'pandas', 'gspread_dataframe', 'oauth2client'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.txt').read(),
)