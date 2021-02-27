# Contributing Guidelines
Contributions to this project are welcome. Do note that this service is essential to our internal infrastructure, which means that the quality requirements are high.

## Reporting bugs
If you've found a bug in this project, please open an issue on GitHub. Describe the bug, the steps required to reproduce the bug, and, if possible, a few lines of code to demonstrate the bug. This makes it easy for us review your bug report.

## Proposing new features
If you'd like to propose a new feature or a change to an existing feature, please open an issue on GitHub describing your proposal. As this project is an integral part of our infrastructure, all changes need to be approved, ideally before someone has put a lot of effort into implementing the change. Change management is very important for this project.

If your proposed change affects API-endpoints, please include your initial design for the new contract of the API-endpoint. To make this a bit easier, we've created an issue template with an example of such a contract. If you're only changing a small part of an endpoint, it's fine to only include the relevant changes. This makes it easier for us to estimate the impact your change will have on other services: Do we need to make a lot of changes to other services to account for this change?

## Submitting Code
You can submit changes to the project using a Pull Request on GitHub. Please make sure to include all relevant information in your Pull Request description, including the reason for making the change and the GitHub Issue linked to this Pull Request. Pull Requests that change existing endpoints or introduce new endpoints should also include a clear overview of the endpoints involved, as we need to make sure that other services in our infrastructure are prepared for the changes.

### Commit History
We value a clear and documenting commit history. This means that each commit should contain a single, atomic change and clear commit message describing the change, including the intentions behind the change and non-obvious design decisions. Please make sure that your commit history is clean before opening your Pull Request.

As a very general guideline for commit messages, the summary line of your commit message should be no longer than 50 characters; the body of your commit message should be hard-wrapped at 72 characters.

We've compiled a few resources on making good commits:

- https://chris.beams.io/posts/git-commit/
- https://thoughtbot.com/blog/5-useful-tips-for-a-better-commit-message
- http://ablogaboutcode.com/2011/03/23/proper-git-commit-messages-and-an-elegant-git-history
- https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
- https://dhwthompson.com/2019/my-favourite-git-commit

### Code Style
We value a clear and consistent code style throughout our project. While linting isn't all that matters for writing clean code, we mostly follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/). The best way to check if your code complies to our style standards is by running our linting setup. We use `flake8`, with several plugins, and `black` to ensure some consistency across different authors.

You can run those tools, with the settings we've configured, by first installing the development environment defined in our [`Pipfile`](Pipfile) with `pipenv sync --dev` and then by running `pipenv run lint`.

### Test Coverage
You may think of an API-endpoint as offering a contract: If a client sends a certain request, the API will respond in a certain way. These types of contracts are highly testable and that's why we require tests for all API-endpoints. The resulting test suite will be run automatically in our Continuous Integration pipeline, but you should also make sure to run tests locally before pushing your code. These tests will help us to make sure a change doesn't break something, even if that something is unrelated to the chance at a first glance.

## Code of Conduct
This is a Python Discord project. As such, it falls under the [Python Discord Code of Conduct](https://pythondiscord.com/pages/code-of-conduct/). Make sure that you are familiar with our Code of Conduct before contributing to this project.

## License
By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE) located in the root directory of the repository.
