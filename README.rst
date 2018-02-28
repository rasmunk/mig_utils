.. image:: https://travis-ci.org/rasmunk/mig_utils.svg?branch=master
    :target: https://travis-ci.org/rasmunk/mig_utils
.. |br| raw:: html

   <br />

=========
mig_utils
=========

A Minimum Intrusion Grid(MiG) utilities python library: |br|
Includes the mig.io module that provides access to MiG Sharelinks through python.

------------
Installation
------------

Installation from pypi::

    pip install mig-utils

Installation from a local git repository::

    cd mig-utils
    pip install .

-------
IO Example
-------

ERDA (https://erda.dk) sharelink access with python3 example::
  
  # First import the class that gives you access to the share in question*
  from mig.io import ErdaShare
  
  # Initialize sharelink
  share = ErdaShare('SHARELINKID')
  
  # List files/dirs in share
  print(share.list())
  
  # Read file directly as string
  print(share.read('tmp'))
  
  # Read file directly as binary
  print(str(share.read_binary('tmp')))
  
  # Get a _io.TextIOWrapper object with automatic close
  with self.share.open('tmp', 'r') as tmp:
    print(tmp.read())

  # Get a default _io.TextIOWrapper object with manual lifetime
  file = share.open('tmp', 'r')
  print(file.read())
  file.close()

A likewise sharelink class exists for IDMC (https://idmc.dk)
