# Death Star Backend - Millenium Falcon

The Death Star Backend project aka Millenium Falcon is an ASGI backend application written in Python to analyse/compute if it is possible to save Endor from Death Star.

This project is part of Giskard technical test.

## Getting started

### Prerequisites
- Python 3.10
- PDM 2.1

You need first to install PDM by following [PDM documentation](https://pdm.fming.dev/latest/#installation).

Then at the root directory type the following command in your terminal:

```bash
pdm install
```

### Usage
You need to create an *.env* file in the root directory. Hereafter a typical DEV environement configuration:

```bash
APP_HOST=127.0.0.1
APP_PORT=8000
APP_RELOAD=True
CORS_ALLOW_ORIGINS=*
```

You also need to create a *millennium-falcon.json* file in the root directory like the following one:

```json
{
    "autonomy": 6,
    "departure": "Tatooine",
    "arrival": "Endor",
    "routes_db": "db/universe.sqlite"
}
```

Finally launch it:
```bash
pdm start_server
```

## Git branching model and workflow

To work efficiently together with Git, OneFlow has been chosen. See [OneFlow – a Git branching model and workflow](https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow).

Because this repository is using 2 branches (develop and main), the chosen workflow is the variation with 2 branches with Option #3 to finish a feature branch.
