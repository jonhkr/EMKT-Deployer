from setuptools import setup, find_packages

install_requires = ['ftputil']

setup(name='EMKT-Deployer',
      version='0.0',
      description=('Upload to FTP and litmus your email marketing'),
      keywords='',
      author="Jonas Trevisan",
      author_email="jonhkr@gmail.com",
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      install_requires = install_requires
    )