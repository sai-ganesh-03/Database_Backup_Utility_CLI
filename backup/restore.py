import subprocess
import sqlite3
import logging
import os
import tarfile
import gzip
import shutil

def decompress_backup(backup_file):
    """
    Decompress a compressed backup file.

    :param backup_file: The path to the compressed backup file
    :return: The path to the decompressed SQL file
    """
    if backup_file.endswith('.tar.gz'):
        decompressed_file = backup_file[:-7]  # Remove .tar.gz
        with tarfile.open(backup_file, "r:gz") as tar:
            tar.extractall(path=os.path.dirname(backup_file))
        return decompressed_file

    elif backup_file.endswith('.gz'):
        decompressed_file = backup_file[:-3]  # Remove .gz
        with gzip.open(backup_file, 'rb') as f_in:
            with open(decompressed_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return decompressed_file

    else:
        return backup_file  # Not compressed, return the original file


def restore_backup(db_type, backup_file, config, logger):
    """
    Restore a backup of the specified database type.

    :param db_type: Type of the database (mysql, postgresql, mongodb, sqlite)
    :param backup_file: Path to the backup file to restore from
    :param config: Dictionary containing connection parameters
    :param logger: Logger instance for logging restore operations
    """
    try:
        # Decompress the backup file if it's compressed
        decompressed_file = decompress_backup(backup_file)

        if db_type == "mysql":
            # Run the mysql command to restore from the backup file
            command = ["mysql", "-u", config['user'], "-p" + config['password'], "-h", config.get('host', 'localhost'), "-P", str(config.get('port', 3306)), config['database']]
            with open(decompressed_file, 'r') as f:
                subprocess.run(command, stdin=f, check=True)
            logger.info(f"MySQL database '{config['database']}' restored successfully from '{decompressed_file}'.")

        elif db_type == "postgresql":
            command = ["pg_restore", "-U", config['user'], "-h", config.get('host', 'localhost'), "-p", str(config.get('port', 5432)), "-d", config['database'], "-v", decompressed_file]
            subprocess.run(command, check=True)
            logger.info(f"PostgreSQL database '{config['database']}' restored successfully from '{decompressed_file}'.")

        elif db_type == "mongodb":
            command = ["mongorestore", "--host", config.get('host', 'localhost'), "--port", str(config.get('port', 27017)), "--db", config['database'], decompressed_file]
            subprocess.run(command, check=True)
            logger.info(f"MongoDB database '{config['database']}' restored successfully from '{decompressed_file}'.")

        elif db_type == "sqlite":
            conn = sqlite3.connect(config['database'])
            with open(decompressed_file, 'r') as f:
                conn.executescript(f.read())
            conn.commit()  # Ensure changes are committed
            conn.close()
            logger.info(f"SQLite database '{config['database']}' restored successfully from '{decompressed_file}'.")

        else:
            logger.error(f"Unsupported database type: '{db_type}'")
            raise ValueError(f"Unsupported database type: {db_type}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred during restoration of '{config['database']}' with {db_type}: {e}")
        raise
    except sqlite3.Error as e:
        logger.error(f"SQLite error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during restoration: {e}")
        raise
