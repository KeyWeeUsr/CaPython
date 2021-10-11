.. -*- fill-column: 79; mode: rst; eval: (flyspell-mode) -*-

=========================================
CaPython - Python interpreter for Camunda
=========================================

*************
Prerequisites
*************


.. |gpghow| replace:: (how)
.. _gpghow: https://docs.github.com/en/github/authenticating-to-github/managing-commit-signature-verification/generating-a-new-gpg-key

#. GPG key associated with your GitHub account |gpghow|_
#. CLA signed

How to sign CLA
===============

#. Fork the repository
#. Clone the fork locally - ``git clone https://github.com/<you>/CaPython``
#. Visit the `CLA.rst` document in the repository
#. Read the document
#. Add a row with your data
#. Commit the changes and sign the commit
   (``git commit -m "message" --gpg-sign``)
#. Push the changes to your fork
#. Open a pull request in CaPython repository

********************************
Create a development environment
********************************

.. |venv| replace:: ``virtualenv``
.. _venv: https://virtualenv.pypa.io/en/latest/

For CaPython it's okay just to use a |venv|_ package, however to fully test
whether everything works as it should, using Docker is recommended as the
project is distributed mainly as Docker images and the environment variables
used for configuration are split so some apply for the starter code and some
only for the runtime alone.

At the same time, it's targeting to be mainly compatible with Camunda's Docker
image for BPM Platform image, not with the raw executables or JARs, but it the
compatibility is possible, it should be implemented.

Linux and MacOS
===============

#. ``cd <cloned-repo>``
#. ``python -m virtualenv ~/env_capython``
#. ``source ~/env_capython/bin/activate``
#. ``pip install -r dev-requirements.txt``

Windows
=======

#. ``cd <cloned-repo>``
#. ``python -m virtualenv %USERPROFILE%\env_capython``
#. ``%USERPROFILE%\env_capython\bin\activate``
#. ``pip install -r dev-requirements.txt``

*****************************************
Modify some files and open a pull request
*****************************************

#. Modify a file
#. Add a file with changes - ``git add <file>``
#. Check the style by running - ``python style.py``
#. Commit the changes using - ``git commit -m "message" --gpg-sign``
#. Verify the commit(s) are changed with - ``git log --show-signature``
#. Push the changes to your fork - ``git push``
#. Navigate to https://github.com/KeyWeeUsr/CaPython/pulls
#. Create a new pull request (don't forget to describe your changes)
#. Wait for review (adjust after review if necessary)
#. Wait for the merge

*******************
Commit naming guide
*******************

Use these tags for small/atomic commits to distinguish between various code
patches:

* ``[INIT]`` - the first commit in the repo
* ``[CLA]`` - CLA related commits (signing, merging)
* ``[ADD]`` - new features, files, etc
* ``[FIX]`` - fixing a bug or incorrectly implemented behavior
* ``[DEL]`` - only removing line(s)/file(s)
* ``[REF]`` - patches related to large code or behavior refactoring that might
  break compatibility
* ``[SUB]`` - git submodule related changes

Examples::

    [INIT] Add initial empty commit
    [CLA] <username> signed
    [ADD] Add new special variable
    [FIX] Fix passing values into task's runtime
    [DEL] Remove deprecated code
    [REF] Split single large file into package/modules
    [SUB] Add submodule for X
