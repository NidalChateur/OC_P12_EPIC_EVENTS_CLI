[![Windows](https://img.shields.io/badge/Windows-11-blue.svg?logo=Powershell)](https://www.microsoft.com/fr-fr/windows)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1-blue.svg?logo=Powershell)](https://learn.microsoft.com/fr-fr/powershell/scripting/overview?view=powershell-7.4)

[![Python](https://raw.githubusercontent.com/NidalChateur/badges/779ce02cc0ce5bdc16ca2fe297b1229d4e5068d3/svg/python.svg)](https://www.python.org/) 
[![Poetry](https://img.shields.io/badge/poetry-1.7.1-blue.svg?logo=Poetry)](https://python-poetry.org/)
[![Sentry](https://img.shields.io/badge/sentry-logs-purple.svg?logo=Sentry)](https://sentry.io/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Pytest](https://github.com/Nidalchateur/test_github_action/actions/workflows/pytest.yml/badge.svg)](https://github.com/NidalChateur/OC_P12_EPIC_EVENTS_CLI/actions)
[![Flake8](https://github.com/Nidalchateur/test_github_action/actions/workflows/flake8.yml/badge.svg)](https://github.com/NidalChateur/OC_P12_EPIC_EVENTS_CLI/actions)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/12a4581869cb4c9cb4930745da6dd948)](https://app.codacy.com/gh/NidalChateur/OC_P12_EPIC_EVENTS_CLI/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![codecov](https://codecov.io/gh/NidalChateur/OC_P12_EPIC_EVENTS_CLI/graph/badge.svg?token=NHFGB57WWL)](https://codecov.io/gh/NidalChateur/OC_P12_EPIC_EVENTS_CLI)

# EPIC EVENTS CRM 


Epic Events is a company that organizes events (parties, professional meetings, off-site gatherings) for its clients.

The CRM software enables the collection and processing of client data and their events, while facilitating communication between different departments of the company.

Command-line user interface.



## Database schema
 - <a href="https://github.com/NidalChateur/OC_P12_EPIC_EVENTS/blob/main/mission/schema_bdd.pdf">Epic Events database schema</a> 

## Use cases

#### General Requirements

- Each employee must have their own credentials to access the platform.

- Each employee is associated with a role (based on their department).

- The platform should allow for the storage and updating of information regarding clients, contracts, and events.

- All employees should have read-only access to all clients, contracts, and events.

#### Use Cases for Management User

1. Create, update, and delete employees in the CRM system

2. Create and modify all contracts.

3. Filter the display of events, for example: show all events that do not have an associated "support."

4. Modify events (to associate a support employee with the event).

#### Use Cases for Sales User

1. Create clients (the client will be automatically associated with them)

2.  Update clients they are responsible for.

3.  Modify/update contracts for clients they are responsible for.

4. Filter the display of contracts, for example: show all contracts that are not yet signed, or that are not fully paid.

5. Create an event for one of their clients who has signed a contract.

#### Use Cases for Support User

1. Filter the display of events, for example: show only the events assigned to them.

2. Update the events they are responsible for.


## Install

### 0. Get Python and Git

* [Python](https://www.python.org/downloads/)
* [Git](https://git-scm.com/book/en/v2)


### 1. Clone
```
git clone https://github.com/NidalChateur/OC_P12_EPIC_EVENTS_CLI.git
cd OC_P12_EPIC_EVENTS_CLI
```
### 2. Create the virtual env

```
python -m venv env
```

### 3. Create the virtual env

- Windows : `env\Scripts\activate.bat`
- Unix/MacOS : `source env/bin/activate`
   
### 4. Install poetry

```
pip install poetry
```

### 4. Install dependencies

```
poetry install
```

### 5. Run

```
poetry run python main.py
```


## Activate Sentry

In the .env file automatically created after the application starts, add the [Sentry](https://https://sentry.io/) key to the SENTRY_DSN variable without quotation marks.
