# findMyJob
This project contains Python scripts to scrape job data from LinkedIn, Indeed, and Rekrute. The data is saved into CSV and Excel files.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- `pip` (Python package installer)
- Latest version of [Google Chrome]. To update it, Open Google Chrome then Click the three vertical dots (Menu) in the top-right corner, select `Help` > `About Google Chrome` and Chrome will automatically check for updates and install them. After the update, click `Relaunch`.

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/zaim001/findMyJob.git
    cd findMyJob
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## LinkedIn Job Scraper

The LinkedIn job scraper script (`linkedin-jobs.py`) collects job data from LinkedIn.

### Usage

1. Run the script:

    ```sh
    python linkedin-jobs.py
    ```

2. Follow the prompts to enter the job title and location.

3. The script will scrape the job data and save it into `linkedin.csv` and `linkedin.xlsx`.

### Note

The number of scrapped linkedin jobs is limited.

## Indeed Job Scraper

The Indeed job scraper script (`indeed.py`) collects job data from Indeed

### Usage

1. Run the script:

    ```sh
    python indeed.py
    ```

2. Follow the prompts to enter the job title and location.

3. The script will scrape the job data and save it into `indeed.csv` and `indeed.xlsx`.

## Rekrute Job Scraper

The Indeed job scraper script (`rekrute.py`) collects job data from Indeed

### Usage

1. Run the script:

    ```sh
    python rekrute.py
    ```

2. Follow the prompts to enter the job title and location.

3. The script will scrape the job data and save it into `rekrute.csv` and `rekrute.xlsx`.
