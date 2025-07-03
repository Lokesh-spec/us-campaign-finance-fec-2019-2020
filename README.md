# US Campaign FEC Data Uploader

This project uploads FEC data files to **MySQL database** and **Google Cloud Storage (GCS)** based on a YAML configuration. It supports bulk ingestion, and initial data cleaning via a Jupyter notebook.

---

## Project Structure

``` bash
├── config/
│   └── config.yaml                # YAML config with MySQL, GCS info and file mapping
├── credentials/
│   └── gcs_credentials.json       # GCS service account key
├── notebooks/
│   └── data_cleaning_us_campaign.ipynb  # [ADDED] Data cleaning logic for selected datasets
├── src/
│   ├── filessio_uploader.py       # MySQL uploader logic
│   ├── gcs_uploader.py            # [ADDED] GCS uploader logic
│   └── init.py
├── main.py                        # Pipeline orchestrator script
├── requirements.txt               # Python dependencies
├── .gitignore
└── README.md

```

---

## Setup

1. **Create and activate a Python virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. **Install dependencies:**

    ```bash
    uv pip install -r requirements.txt
    ```

3. **Configure MySQL and GCS settings in `config/config.yaml`:**

    ```yaml
    mysql:
      host: your_mysql_host
      port: 3306
      username: your_username
      password: your_password
      database: your_database

    gcs:
      bucket: your_bucket_name
      upload_folder: bronze-layer
      credentials_file: credentials/gcs_credentials.json

    fec_data_files:
      - file: "data/ccl.txt"
        table_name: "candidate_committee_linkage"
        columns:
          - "CAND_ID"
          - "CAND_ELECTION_YR"
          - "FEC_ELECTION_YR"
          - "CMTE_ID"
          - "CMTE_TP"
          - "CMTE_DSGN"
          - "LINKAGE_ID"
      - file: "data/cm.txt"
        gcs_folder: "committee-master"
      # ...
    ```

---

## Usage

Run the main pipeline:

```bash
python main.py
```

This will:
- Upload files defined with columns to MySQL
- Upload files without columns to GCS
- Read paths, database credentials, and GCS settings from config.yaml

---

## Data Cleaning [ADDED]

A notebook is provided to clean FEC datasets:

📍 notebooks/data_cleaning_us_campaign.ipynb

Currently implemented:
- weball20.txt – All Candidates Summary
- cn.txt – Candidate Master File

Cleaning includes:
- Handling missing values
- Data type casting
- Enriched the data
- Removing invalid records
- Saving cleaned DataFrame to Silver Layer on GCS Bucket

---

## Notes

- Ensure the MySQL user has permissions to create/drop tables and insert data.
- The columns specified in the config must exactly match the columns in your data files.
- Data files are expected to be pipe (|) separated and do not include headers; columns are assigned from the config file.
- Column names with special characters (like hyphens -) are handled with backticks in SQL queries.

---

## FEC Data File Abbreviations (2019–2020 Cycle)

| Filename     | Stands For                          | Description                                                                                    |
| ------------ | ----------------------------------- | ---------------------------------------------------------------------------------------------- |
| ccl.txt      | Committee Candidate Linkage         | Links committees to the candidates they support.                                               |
| cm.txt       | Committee Master File               | Details about political committees (type, designation, treasurer, etc.).                       |
| cn.txt       | Candidate Master File               | Basic info about candidates (name, office, party, district, etc.).                             |
| indiv20      | Individual Contributions            | Directory containing individual contribution files.                                            |
| itoth.txt    | Other Itemized Transactions         | Contributions to committees other than from individuals or PACs (e.g. party, candidate loans). |
| itpas2.txt   | Itemized PAC Contributions          | PAC contributions to candidates/committees.                                                    |
| oppexp.txt   | Operating Expenditures              | Detailed records of money committees spent on operations.                                      |
| webk20.txt   | Candidate Key File (Web Format)     | Key linking for web-based data presentation (crosswalk of IDs).                                |
| weball20.txt | All Candidates (Web)                | Candidate summary file (expenditures, receipts, etc. used on FEC’s website).                   |
| webl20.txt   | Candidate-Committee Link File (Web) | Another format of candidate-committee links, used for FEC.gov site backend.                    |


---

## 📂 Official FEC Bulk Data Source

You can find the original Federal Election Commission bulk data files at:

👉 [FEC-Data-Link](https://www.fec.gov/data/browse-data/?tab=bulk-data)

This project uses files from that source for the 2019–2020 election cycle.

--- 

## Troubleshooting
- Column mismatch: Check that config column count matches actual data for MySQL data upload.
- MySQL errors: Make sure column names are backtick-quoted and not using reserved keywords.
- GCS auth issues: Confirm that the service account JSON key is valid and bucket exists.
- Wildcard issues: Ensure the path in fec_data_files is correct (e.g., *.txt instead of .csv).

--- 

## Contributing & Support
- Open issues for bugs or improvement ideas
- Pull requests are welcome!