# SqliteDB Persistence provider for LiteFlow

Provides support to persist workflows running on LiteFlow to a SqliteDB database.

## Installing

Install the "liteflow.providers.sqlite" package

```
> pip install liteflow.providers.sqlite
```

## Usage

Pass an instance of MongoPersistenceProvider to `configure_workflow_host` when configuring your workflow node host.

```python
from liteflow.core import *
from liteflow.providers.sqlite import SqlitePersistenceProvider

sqlite = SqlitePersistenceProvider('liteflow.db')

host = configure_workflow_host(persistence_service=sqlite)
host.start()

```
