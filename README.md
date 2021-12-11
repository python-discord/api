# :warning: ARCHIVED :warning:

Python Discord Core Developers have decided not to pursue further development of the API project.

<details>
  <summary>Read more</summary>
  The Core Developer and Admin teams have decided to halt further work on rewrite of the Python Discord API from Django to FastAPI and sunset the python-discord/api repository.

We initially set out on this project to have a simpler API which we hoped to gain more visibility into (monitoring/observability) and reduce the entry requirements for contribution to the project.

We believe that we'd achieved these goals with the current site stack without requiring a rewrite to a different framework, citing some examples:
- We have deployment previews of all static content on pythondiscord.com (e.g. resources, guides, events, etc.). Thanks Scaleios!
- We've installed tooling that allows us to monitor the performance of Django with our existing Prometheus monitoring stack. Thanks Volcyy!
- We've removed the need for subdomains for site, meaning that contribution no longer requires modifications to /etc/hosts or any complex host setup, localhost works! Thanks to me and Volcyy 😎!

Django is a stack which our Core Developers and Contributors are already familiar with, it also has a considerably larger user group, more active maintenance and many more third party extensions. We've still got improvements to make to the current Python Discord site & API, for example improving performance on queries that look at vast amounts of data (e.g. metricity user data), but a migration to a different framework would not necessarily solve these problems.

We'll be archiving the python-discord/api repository shortly, all open PRs have been closed already
  </details>

<h1 align="center">Python Discord API</h1>

<p align="center">
<a href="https://pythondiscord.com"><img alt="Python Discord Website" src="https://raw.githubusercontent.com/python-discord/branding/master/logos/badge/badge_github.svg"></a>
</p>

The Python Discord API is an internal API that serves as an abstraction layer between our [Discord bot](https://git.pythondiscord.com/bot) and our PostgreSQL database.The API is not publicly accessible, but only reachable from within our Kubernetes-cluster.

As it is tightly coupled with the functionality of our bot, the API is currently not strictly versioned and may change at any time depending on the features required for our Discord bot.

## Contributing to the API project

Contributions are welcome.

Do note that this project is essential to our internal services. That's why the quality requirements are high and all pull requests will be reviewed as such. In addition, all API endpoints require full test coverage to guarantee the contracts they offer and code style consistency is enforced with both `flake8` and `black`.  

For more information about contribution to this project, read the [CONTRIBUTING.md](CONTRIBUTING.md) file for this project.

### Proposing new features and endpoints

If you want to propose new features for this API, please open an issue in the Issues-tab in this repository. If your proposal includes a new API endpoint or changes an existing one, please include your initial design for the contract this endpoint offers in your issue. We've created an issue template to give you an idea of how such an issue may look.

### Setting up a development environment
The easiest way to set up a development environment is by using [`poetry`](https://python-poetry.org/). After installing `poetry`, simply run `poetry install` in the root of the cloned repository to set up a virtual environment with our development toolkit installed.

Another option is by using [Docker](https://www.docker.com/). After installing Docker on your machine, you should be able to run the API with `docker compose up`. For older versions of Docker, you may have to install `docker-compose` separately and run `docker-compose up` instead. This should spin up a container that automatically reloads the API if you change one of the files.

### Generating a migration file
With the project running in docker, open another terminal and run `poetry run task revision "Migration message here."`

This will create a migration file in the path `alembic/versions`. Make sure to check it over, and fix any linting issues.
