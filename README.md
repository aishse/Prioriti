# Prioriti

CS122 Semester Project  
**Authors:** Anishka Chauhan, Bineet Anand

A Pomodoro timer and task management web application built with Flask, Tailwind CSS, and SQLite.

---

## Table of Contents

- [Prioriti](#prioriti)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a Virtual Environment (Recommended)](#2-create-a-virtual-environment-recommended)
    - [3. Install Python Dependencies](#3-install-python-dependencies)
    - [4. Install Node.js Dependencies](#4-install-nodejs-dependencies)
  - [Running the Application](#running-the-application)
    - [1. Build Tailwind CSS](#1-build-tailwind-css)
    - [2. Start the Flask Server](#2-start-the-flask-server)
  - [Building Tailwind CSS](#building-tailwind-css)
    - [One-Time Build (Minified)](#one-time-build-minified)

---

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python 3.11+** (check with `python3 --version`)
- **Node.js & npm** (check with `node --version` and `npm --version`)
- **Conda** (optional, for virtual environment management)

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Prioriti
```

### 2. Create a Virtual Environment (Recommended)

Using conda:
```bash
conda create -n prioriti-env python=3.11
conda activate prioriti-env
```

Or using venv:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install flask sqlalchemy
```

### 4. Install Node.js Dependencies

```bash
npm install
```

This installs Tailwind CSS, PostCSS, and Autoprefixer as development dependencies.

---

## Running the Application

### 1. Build Tailwind CSS

Before starting the server, compile the Tailwind CSS:

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --minify
```

**Or** use the npm script for watch mode (auto-rebuilds on file changes):

```bash
npm run watch:css
```

This command will continuously monitor your CSS files and rebuild automatically whenever you make changes.

### 2. Start the Flask Server

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5001`

---

## Building Tailwind CSS

### One-Time Build (Minified)

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --minify
```