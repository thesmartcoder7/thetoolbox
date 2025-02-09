# ![Alt text](doc-images/toolbox.svg) TheToolbox

![Alt text](doc-images/ui.png)

## Overview

The **All-in-One Toolbox** is a powerful suite of tools designed to help users analyze and optimize websites, domains, and repositories. It provides a range of functionalities such as SSL checks, security headers analysis, domain health assessments, DNS configurations, github repository analyzer and more.

## Features

- **Domain Checker** – Verify SSL status and expiration.
- **Website Security Headers** – Inspect HTTP security headers to identify potential vulnerabilities.
- **Domain Health Check** – Assess DNS resolution, email deliverability, and website accessibility.
- **WHOIS Lookup** – Retrieve domain registration and ownership details.
- **DNS Configuration** – Fetch domain DNS records, including A, CNAME, MX, TXT, and NS records.
- **PageSpeed Insights** – Analyze website performance and receive optimization suggestions.
- **GitHub Repository Analyzer** – Evaluate GitHub repositories for optimization issues.
- **And Many More** – Additional tools for website and domain analysis.

## Installation

### Prerequisites

Ensure you have the following installed:

- Node.js (if applicable)
- Python (if applicable)
- Docker (if running in a containerized environment)

### Clone the Repository

```sh
git clone https://github.com/thesmartcoder/thetoolbox.git
cd thetoolbox
```

### Install Dependencies

Installing dependencies can be done the manual way or through the scripts provided for ease of use. The script does everything including running the application for you.

1. manual

```sh
# install the frontend dependencies
cd frontend
npm install

# install  the backend dependencies
cd ../backend
python3 -m venv .venv
pip install -r requirements.txt
```

2. Using the bash script

```sh
# make script excecutable
chmod +x devstart
./devstart
```

### Run the Application

1. Manual

```sh
cd frontend
ng serve -o # serves the frontend on localhost:4200

cd backend
python3 manage.py runserver  # serves the backend on localhost:8000
```

2. Using the bash script

```sh
# make script excecutable
chmod +x devstart
./devstart
```

3. Using docker-compose

```sh
sudo docker-compose up --build
```

There is another script for forcing the docker compose to run after making all the checks.

```sh
./deploy
```

## Usage

1. Start the application.
2. Access the toolbox via the web interface.
3. Select the desired tool (e.g., Domain Checker, WHOIS Lookup).
4. Enter the required information (domain name, repository URL, etc.).
5. View the results and take necessary actions.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Make your changes and commit them.
4. Push the changes and create a Pull Request.

## License

This project is licensed under the [Apache License Version 2.0](LICENSE).

## Contact

For any inquiries, please contact **samuel.martins4.sm@gmail.com** or open an issue on GitHub.

## Acknowledgments

Special thanks to all contributors and open-source libraries used in this project.

---

_Developed and maintained by [Samuel Martins](https://github.com/thesmartcoder7)._
