import os


# Whether the app runs in a Docker container
_DOCKER_VAR = os.getenv("DOCKER")

IN_DOCKER = False
if _DOCKER_VAR == "true":
    IN_DOCKER = True


DATABASE_URL = "sqlite:///data/jobs.db"
if IN_DOCKER:
    DATABASE_URL = f"sqlite:////data/jobs.db"