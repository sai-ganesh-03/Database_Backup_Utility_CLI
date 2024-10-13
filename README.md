
# Database Backup CLI Tool

This CLI tool is designed to facilitate database backup and restoration operations, with support for various database types and cloud storage options. The tool can compress backup files, send notifications via Slack, and log operations for monitoring purposes.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Arguments](#arguments)
   - [Examples](#examples)
4. [Use Cases](#use-cases)
5. [Logging](#logging)


## Features

- Supports multiple database types: MySQL, PostgreSQL, MongoDB, and SQLite.
- Backup and restore operations.
- Optional backup compression.
- Upload backups to cloud storage providers (AWS S3, Google Cloud Storage, Azure).
- Slack notifications for successful operations.
- Logging for tracking operations and troubleshooting.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sai-ganesh-03/Database_Backup_Utility_CLI.git
   cd Database_Backup_Utility_CLI
   ```

2. **Install dependencies**:
   Ensure you have Python 3.x installed. You can use pip to install necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your `config.json` file**:
   Create a `config.json` file in the project directory with the following structure:
   ```json
   {
       "database": {
           "host": "localhost",
           "port": 3306,
           "user": "your_username",
           "password": "your_password",
           "database": "your_database"
       },
       "aws": {
           "access_key": "your_access_key",
           "secret_key": "your_secret_key"
       },
       "gcs": {
           "service_account_key": "path_to_your_service_account_key.json"
       },
       "azure": {
           "connection_string": "your_connection_string"
       },
       "slack_webhook":"https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
   }
   ```

## Usage

To use the database backup CLI tool, run the script with the desired operations and arguments. The basic syntax is:

```bash
python backup_cli.py [operation] [options]
```

### Arguments

- **operation**: Choose from `backup` or `restore`.
- **--db-type**: Specify the type of database (`mysql`, `postgresql`, `mongodb`, `sqlite`).
- **--config**: Path to the JSON configuration file for database connection.
- **--output**: Path for the output backup file (only for backup operation).
- **--compress**: Add this flag to compress the backup (only for backup operation).
- **--backup-file**: Path to the backup file for restoration (only for restore operation).
- **--cloud**: Specify the cloud storage option (`s3`, `gcs`, `azure`).
- **--bucket**: Name of the cloud storage bucket (required if cloud is specified).
- **--log-file**: Path to the log file (default is `backup.log`).

### Examples

#### 1. Backup a MySQL Database

To backup a MySQL database and store the backup file as `my_database_backup.sql`, use the following command:

```bash
python backup_cli.py backup --db-type mysql --config config.json --output /path/to/my_database_backup.sql --compress --cloud s3 --bucket my_backup_bucket --slack-webhook https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX --log-file /path/to/my_database_backup.log
```

#### 2. Restore a MySQL Database

To restore a MySQL database from a backup file:

```bash
python backup_cli.py restore --db-type mysql --config config.json --backup-file /path/to/my_database_backup.sql --slack-webhook https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX --log-file /path/to/my_database_backup.log
```

#### 3. Backup a PostgreSQL Database without Compression

To backup a PostgreSQL database without compression:

```bash
python backup_cli.py backup --db-type postgresql --config config.json --output /path/to/my_postgresql_backup.sql
```

#### 4. Backup and Upload to Google Cloud Storage

To backup and upload to Google Cloud Storage:

```bash
python backup_cli.py backup --db-type mongodb --config config.json --output /path/to/my_mongodb_backup.bson --cloud gcs --bucket my_gcs_bucket
```

#### 5. Restore from an SQLite Backup

To restore an SQLite database from a backup file:

```bash
python backup_cli.py restore --db-type sqlite --config config.json --backup-file /path/to/my_sqlite_backup.db
```

## Use Cases

1. **Regular Backups**: Schedule regular backups of your databases to ensure data safety. Use the `--compress` option to save space.

2. **Cloud Storage Integration**: Automatically upload your backups to cloud providers like AWS, GCS, or Azure for redundancy and disaster recovery.

3. **Notifications**: Set up Slack notifications to keep your team informed about backup and restore operations.

4. **Multi-Database Support**: Use the tool with different database types (MySQL, PostgreSQL, MongoDB, SQLite) for diverse application environments.

## Logging

The tool logs all operations to a specified log file (default: `backup.log`). You can monitor this file to review the operation history and any errors encountered during execution.
