# mp-events-hub
Microservice built with FastAPI to retrieve TRON address information: TRX balance, bandwidth, and energy.

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yoocontext/mp-events-hub.git
2. **Start the infrastructure in Docker:**
   ```bash
   make pg
   make app
if you don't have `make`, you can run the commands directly from the comments under each target in the Makefile.
3. **Run migrations**
    ```bash
   cd app
   alembic upgrade head
4. **Manually populate initial data, e.g., create `user` and `admin` roles in `pg.roles`.**
4. **Install all required packages in `pyproject.toml` section.**


### Implemented Commands

* `make app` - up application
* `make pg` - up database
* `pytest` - test application with pytest