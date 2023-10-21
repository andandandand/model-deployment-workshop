# Understanding the relationship between GNU Make and Docker Compose

[Docker Compose](https://docs.docker.com/compose/) is a tool used to define and run multi-container Docker applications. You define the setup of your application's services, networks, and volumes in a `docker-compose.yml` file, and then use the `docker-compose` command-line tool to build, start, and manage those services.

Makefiles, on the other hand, are a build automation tool from [GNU Make](https://www.gnu.org/software/make/) used to compile source code into binary files. GNU Make is a tool which controls the generation of executables from the program's source. Make gets the knowledge about how to build the executable from the Makefile. 

In this repo, [we have defined a set of `docker-compose` operations on a Makefile](https://github.com/andandandand/model-deployment-workshop/edit/master/markdown_notes/Understanding%20Makefiles%20in%20Docker%20Compose.md#:~:text=Dockerfile-,Makefile,-README.md). 

We use a `Makefile` through the `make` command to specify how to create the target program. Although originally designed for compiling programs, you can use `make` for any task where you need to turn 'source' files into 'output' files following a set of rules.

When you're working on a project that uses Docker Compose, it's common to run a series of Docker Compose commands like `docker-compose build`, `docker-compose up`, `docker-compose down`, etc. You can automate these steps using a Makefile, making it easier and more straightforward to manage your project.

### Example Scenario

Let's say you commonly perform the following tasks in your Docker Compose project:

1. Build the Docker images
2. Start the Docker containers
3. Stop the Docker containers

You can define these tasks in a Makefile as follows:

```make
build:
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down
```

With this Makefile, instead of remembering and typing out the full Docker Compose commands, you can simply run:

- `make build` to build your images
- `make start` to start your containers
- `make stop` to stop your containers

By integrating Makefiles with Docker Compose, you streamline the workflow, making it easier to manage complex applications. You can even extend this to include tasks like running tests, cleaning up unnecessary files, and other routine tasks.

```make
.PHONY: build

build:

	docker compose build

  

.PHONY: run

run:

	docker compose up
```
A Makefile is a way to manage build and workflow automation. In the given Makefile, there are two targets: `build` and `run`, both marked as `.PHONY`.

- `.PHONY`: This tells `make` that the targets are not associated with any files. Usually, `make` assumes that a target is a file that it should look for, but `.PHONY` says these targets will always run, regardless of any files with the same names.

- `build`: The `build` target uses the command `docker compose build`. When you run `make build`, it triggers Docker Compose to build the services defined in your `docker-compose.yml` file.

- `run`: Similarly, the `run` target uses the command `docker compose up`. Executing `make run` will bring up all the services defined in `docker-compose.yml`, building them first if they have not been built.

To use this Makefile, you can run `make build` or `make run` in the terminal, and it will execute the associated Docker Compose commands, thereby simplifying your workflow.
