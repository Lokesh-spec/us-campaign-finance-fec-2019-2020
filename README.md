# US Campaign FEC Data Uploader

This project uploads CSV data files to a MySQL database. It reads configuration from a YAML file, processes multiple input files, and inserts data into MySQL tables.

---

## Project Structure

├── config/
│ └── config.yaml # YAML config with MySQL credentials and data file info
├── credentials/
│ └── gcs_credentials.json # Credentials for Google Cloud Storage (if used)
├── src/ # Source code for uploader and utilities
├── main.py # Entry point script
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore rules
└── README.md # This file



---

## Setup

1. **Create and activate a Python virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your MySQL connection and data file paths in `config/config.yaml`:**

    ```yaml
    mysql:
      host: your_mysql_host
      port: 3306
      username: your_username
      password: your_password
      database: your_database

    fec_data_files:
      - file: "data/ccl.txt"
        table_name: "candidate_committee_linkage"
        columns:
          - "CAND_ID"
          - "CAND_ELECTION_YR"
          - "FEC_ELECTION_YR"
          - "CMTE_ID"
          - "CMTE-TP"
          - "CMTE_DSGN"
          - "LINKAGE_ID"
      # Add other data files similarly
    ```

---

## Usage

Run the main script:

```bash
python main.py
```

This will:

Read the CSV/TXT files defined in the config.
Create corresponding tables (dropping existing ones if present).
Insert the data into your MySQL database.


## Notes

- Ensure the MySQL user has permissions to create/drop tables and insert data.
- The columns specified in the config must exactly match the columns in your data files.
- Data files are expected to be pipe (|) separated and do not include headers; columns are assigned from the config file.
- Column names with special characters (like hyphens -) are handled with backticks in SQL queries.

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


## Troubleshooting

- Column mismatch errors?
Verify the number of columns in your data files matches your config.
- MySQL syntax errors?
Confirm column names are properly quoted (backticks) and do not conflict with reserved keywords.
- Connection issues?
Ensure MySQL server is running, accessible, and credentials are correct.

## Contributing & Support

Feel free to submit issues or pull requests for improvements!
