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
