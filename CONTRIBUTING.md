# Contributing to Pytch

Thank you for being interested in contributing to Pytch. We strongly encourage any users of Pytch to contribute to it and help improve it. This document was made to:
- Encourage people to contribute
- Offer an easy guide on how to contribute
- Avoid unnecessary processes and save time
- Create more transparency in the development of Pytch

## Bug Reports and Feature Requests

This is the easiest way to contribute to Pytch. Use GitHub issues to report any bugs or request any features. Prefix bug reports with "Bug: " and feature requests with "Feature: ".

Check existing [issues](https://github.com/kritdass/pytch/issues?q=is%3Aissue) before making an issue. We may take some time with addressing issues so please be patient.

For bug reports, please include:
- System Information
- Pytch Version (`pytch -v`)
- Steps to reproduce

## Pull Requests


### Code Guidelines

- Keep code simple and readable
- Use snake_case
   - PascalCase in classes
- Format all code with [`black`](https://github.com/psf/black)
- Should be compatible with Python >=3.7
- Do not add dependencies
    - Reference [neofetch](https://github.com/dylanaraps/neofetch) on getting system information without external dependencies

### Pull Request Codes

<table>
  <tr>
    <th>Code</th>
    <th>Description</th>
    <th>Guidelines</th>
    <th>Examples</th>
  </tr>
  <tr>
    <td>Green 🟢</td>
    <td>A pull request that will nearly always be accepted. This improves the code without modifying existing functionality.</td>
    <td>Make a pull request without hesitation.</td>
    <td>
      <ul>
        <li>Fixing bugs</li>
        <li>Adding support for another system</li>
        <li>Improving code quality (making more readable, adding comments, etc.)</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Yellow 🟡</td>
    <td>A pull request that might be accepted. This modifies functionality in an opinionated way.</td>
    <td>Make an issue first with the prefix "Idea: " and only start working on your pull request when you get approval.</td>
    <td>
      <ul>
        <li>Changing the appearance of the fetch</li>
        <li>Adding a feature</li>
        <li>Changing the structure of the code</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Red 🔴</td>
    <td>A pull request that will almost never be accepted. This modifies functionality in a way that goes against the ideas of the project.</td>
    <td>Do not bother with this idea. If you do want to continue, make your own fetch but follow the terms of our <a href="LICENSE.md">license</a>. If you really think your idea is good, then make an issue with the prefix "Red: ".</td>
    <td>
      <ul>
        <li>Not following <a href="#code-guidelines">code guidelines</a></li>
        <li>Rewriting the program in another language</li>
        <li>Reverting features</li>
      </ul>
    </td>
  </tr>
</table>

### Making the Pull Request

1. Review the [pull request codes](#pull-request-codes), find out which code your pull request comes under, and adhere to its specific guidelines
2. Mention any and all changes, additions, removals, etc. This includes breaking changes and changes in program structure. Document these in the body of your pull request and the [changelog](CHANGELOG.md).
3. We use [SemVer](http://semver.org/) for versioning (only make a patch if you are adding support for a distribution or package manager) and
[Conventional Commits](https://www.conventionalcommits.org/) for commit messages  (all lowercase) as of 1.2.0. Please follow these guidelines in your commits and in your pull request title.
4. Ensure that you are following the [code guidelines](#code-guidelines)
5. Bump the version in `pyproject.toml` and `src/pytch/__main__.py`
6. Remove any files used for testing
7. Make your pull request!

### What should I contribute on?

The best way to find things to contribute on is to go to the [todos](README.md#todos) and find something to work on.

You can also check out our [open issues](https://github.com/kritdass/pytch/issues), which are generally low-hanging fruit for contributions.
