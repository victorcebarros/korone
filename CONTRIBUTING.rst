Reporting bugs
==============

Prior to creating an issue on GitHub, please check that:

- You are running the latest version of Korone.
- You are using a clean installation of Korone.
- Similar issues haven't been already reported.

After all these conditions were fulfilled, then you should be able
to submit a bug report.

When creating a bug report, you should:

- Briefly describe the bug / unexpected behavior and what would be the correct behavior.
- Explain how to reproduce the issue.
- Provide logs / backtraces, excluding personal information.

How to contribute
=================

There are some basic guidelines you need to understand in order to keep the codebase
consistent and well coordinated.

Getting started
---------------

- You should have a basic understanding of `git`_.

Coding Style
------------

- Follow the `PEP8 Style Guide`_.
- Use docstrings in a concise and cohesive manner, with `pydoc`_ in mind.
- Use `Type Annotations`_.
- Before submitting a new PR, run the tests.

Commit messages
---------------

To maintain consistency, it is important to abide by the following style directives:

- Specify the type of commit
- Separate the type of commit from the brief description with a colon
- Add a brief description after the commit type, separated by a space
- Use a verb on the third-person singular after the commit type
- Capitalize words appropriately
- Don't add a period to the end of the commit message

For the commit types, the following table will help you decide which one you should use:

+-------------+--------------------------+
| Commit Type | Description              |
+=============+==========================+
| Chore       | Regular code maintenance |
+-------------+--------------------------+
| Docs        | Documentation            |
+-------------+--------------------------+
| Feat        | New features             |
+-------------+--------------------------+
| Fix         | Bugfixes                 |
+-------------+--------------------------+
| Merge       | Merge related changes    |
+-------------+--------------------------+
| Refactor    | Refactoring              |
+-------------+--------------------------+
| Style       | Style related changes    |
+-------------+--------------------------+
| Test        | Code testing             |
+-------------+--------------------------+

For example, instead of doing this:

``behavior y for function x has been fixed.``

Do this:

``Fix: Corrects behavior y from function x``

Commits prior to this guideline will be kept, but new commits should follow these recommendations.

Committing changes
------------------

You should try to make commits of logical units, in order to prevent making a
bunch of unrelated changes in a single commit.

Version Numbering
-----------------

We use SEMVER, refer to `semver.org`_ for more detailed information.

.. _git: https://git-scm.com/
.. _PEP8 Style Guide: https://www.python.org/dev/peps/pep-0008/
.. _pydoc: https://docs.python.org/3/library/functions.html#pydoc
.. _Type Annotations: https://www.python.org/dev/peps/pep-0484/
.. _semver.org: https://semver.org/
