# Project Management API

# Overview

This project is an API designed to manage **projects**, which in this context represent **plots of land**.
The API allows users to create, read, update, list, and delete projects. Each project is analyzed using
**satellite imagery** captured within a specified date range.

The API is built using **FastAPI** and persists project data in a **PostgresQL**. The architecture is designed to be
extensible, allowing future additions of endpoints and functionalities.

## Features

- **Create** a new project
- **Read** project details
- **List** all projects
- **Update** an existing project
- **Delete** a project

## Project Attributes

Each project includes the following attributes:

- **name** *(required)* – A short, descriptive name (max **32 characters**).
- **description** *(optional)* – Additional details about the project.
- **date range** *(required)* – The timeframe for satellite imagery analysis.
- **area of interest** *(required)* – A **GeoJSON file** defining the project's geographical boundaries.

### Sample GeoJSON File (Terra\_de\_meio.json)

```json
{
  "type": "Feature",
  "properties": {},
  "geometry": {
    "type": "MultiPolygon",
    "coordinates": [
      [
        [
          [-52.8430645648562, -5.63351005831322],
          [-52.8289481608136, -5.674529420529012],
          [-52.8114438198008, -5.6661010219506664],
          [-52.797327415758296, -5.654301057317909],
          [-52.788292917171, -5.651491506446291],
          [-52.7803877309072, -5.640815088854069],
          [-52.7555428597923, -5.641377010471558],
          [-52.738603174941204, -5.63800547260297],
          [-52.729568676354, -5.631262338119598],
          [-52.719404865443295, -5.626204935899693],
          [-52.709241054532704, -5.616089999567166],
          [-52.6708444355369, -5.569446637469866],
          [-52.6787496218007, -5.558206718303779],
          [-52.687784120388, -5.534602190108217],
          [-52.7098057106944, -5.5390983634896],
          [-52.7244867708986, -5.546404572245265],
          [-52.7600601090859, -5.5722565836830285],
          [-52.7843403240391, -5.584058210883924],
          [-52.8074912266689, -5.589115978388449],
          [-52.823301599196604, -5.618337778382639],
          [-52.8385473155626, -5.620585548523252],
          [-52.8430645648562, -5.63351005831322]
        ]
      ]
    ]
  }
}
```

## Technical Requirements
- **FastAPI**  as the web framework.
- **PostgresQL** database for persistent data storage.


# Running application
 After forking this project into your system, follow those steps to run project locally

---

 ## Configure database
 open psql shell
 ```shell
 psql
 ```

 create database user
 ```shell
 CREATE ROLE projectsmanager WITH LOGIN PASSWORD 'projectsmanager';
 ```

 In order for testcases to run properly you need to add privileges for creating databases, to newly created user
 ```shell
 ALTER USER projectsmanager CREATEDB;
 ```

 create database
 ```shell
 CREATE DATABASE projectsmanager OWNER projectsmanager ENCODING UTF8;
 ```

---

## Setup environment
This project use `Poetry` dependency manager. In order to setup env and install dependencies run:

 ```shell
 poetry install
 ```

To enter newly created poetry env run

```shell
poetry shell
```

### Note
1. There is `requirements.txt` file available in the project, if you prefer to use virtualenv instead of poetry.
2. All commands that will be listed after this, needs to be run from the root of this project, with environment activated

---

## Create `.env` file
 Add `.env` file to the `projects_manager.config` catalogue. You can use `.env-template` file for
 reference

---

 ## Install pre-commit

 ```shell
 pre-commit install
 ```

 ## Run unittests

 ```shell
 pytest
 ```

 ## Run fastapi dev localhost
 ```shell
 fastapi dev
 ```


# API Description

The following endpoints manage projects, including creating, listing, retrieving details, updating, and deleting projects.
Full description of schemas and responses is available in build in FastApi swagger, accessible under `/docs` endpoint

## Endpoints

---

### **Create Project**
`POST /api/projects/create`


### **List Projects**
`GET /api/projects/list`

### **Get Project Details**
`GET /api/projects/details/{project_id}`


### **Update Project**
`PATCH /api/projects/update/{project_id}`


### **Delete Project**
`DELETE api/projects/delete/{project_id}`


### Notes:
- Endpoints use **UUID** for `project_id` as a unique identifier.
- Pagination support is implemented for the `/list` endpoint.
