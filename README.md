# mp-events-hub
Microservice built with FastAPI for backend infrastructure within the “Moscow Polytechnic Extracurricular Activity Platform”.


# About the Project

**mp-events-hub** is a microservice developed as part of the large-scale project **“Moscow Polytechnic Extracurricular Activity Platform”** — a unified digital events hub designed to centralize all extracurricular activities of Moscow Polytechnic University. Its mission is to increase student engagement, simplify coordination, and build a modern interactive digital environment for event participation.


## Project Background

Event announcements within the university are currently scattered across various social networks, which creates information noise and low reach. The main communication channel — a VK community — lacks filtering by interests or dates, and its popularity among students continues to decline.

This leads to low attendance and forces organizers to spend significant manual effort on promotion, especially for large events.

The new digital platform solves these issues by offering:

- a centralized event board for all extracurricular activities;
- structured and unified event listings;
- convenient search and filtering tools;
- personalized content;
- interactive features and elements of gamification;
- transparent motivation and reward mechanics.

The project aims to increase student involvement through a modern, unified digital ecosystem.


## Technology Stack

- **Python** — backend logic  
- **FastAPI** — REST API  
- **Docker** — containerization  
- **PostgreSQL** — shared database infrastructure  
- **Alembic** — database migrations  


## Role in the System Architecture

The full platform is developed by multiple collaborative teams:

- **Backend Team** — Python/FastAPI microservices  
- **Frontend Team** — HTML, CSS, JS dynamic website interface  
- **Design Team** — UI/UX, layouts (Figma, Photoshop)  
- **Database Team** — PostgreSQL schema design and support  

**mp-events-hub** is one of the backend microservices responsible for supporting the platform’s data processing and communication logic.


# How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yoocontext/mp-events-hub.git
   ```

2. **Start the infrastructure in Docker:**   

   ```bash
   make pg
   make app
   ```
   
if you don't have `make`, you can run the commands directly from the comments under each target in the Makefile.

3. **Run migrations**
   
   ```bash
   cd app
   alembic upgrade head
   ```

4. **Manually populate initial data, e.g., create `user` and `admin` roles in `pg.roles`.**

5. **Install all required packages in `pyproject.toml` section.**


## Implemented Commands

* `make app` - up application
* `make pg` - up database
* `pytest` - test application with pytest