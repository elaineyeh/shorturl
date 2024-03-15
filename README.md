# ShortURL

## Get Started For IDE

### Prerequisites

git >= 2.32.0
python >= 3.8.3

### Setting Up the Environment for Development

#### Homebrew

```sh
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update
```

#### Virtual Environments

Download Repository

```sh
git clone [repository]
cd [repository]
```

Set project Python version with 3.8.3

```sh
pyenv local 3.8.3
```

Automatically creates and manages a virtualenv for your projects
Create a new project using Python 3.8

```sh
pipenv --python 3.8.3
pipenv shell
```

Install all dependencies for a project (including dev).

```sh
pipenv install --dev
```

Generate a set of requirements out of it with the default dependencies.

```sh
pipenv requirements > app/requirements.txt
```

## Building Up the Project for Development

### Install Docker

```sh
# Docker
brew install docker docker-compose
open /Applications/Docker.app
```

### Customize the Settings

#### env file

```sh
# Copy web env example file
cp shorturl/.env.example shorturl/.env
```

### Build images, Start containers

```sh
docker-compose -f docker-compose.yml up -d --remove-orphans --build
```
