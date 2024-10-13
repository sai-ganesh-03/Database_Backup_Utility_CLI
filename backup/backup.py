import subprocess

def full_backup(db_type, db_name, config, output_file, logger):
    """
    Perform a full backup of the specified database type.

    :param db_type: Type of the database (mysql, postgresql, mongodb, sqlite)
    :param db_name: Name of the database to back up
    :param config: Dictionary containing connection parameters
    :param output_file: Path where the backup file should be stored
    :param logger: Logger instance for logging backup operations
    :return: The path to the backup file
    """
    try:
        if db_type == "mysql":
            # Create the mysqldump command
            command = ["mysqldump", "-u", config['user'], f"-p{config['password']}", db_name]
            # Open the output file and run the command
            with open(output_file, 'w') as f:
                subprocess.run(command, stdout=f, check=True)
            logger.info(f"MySQL backup of {db_name} completed successfully, saved to {output_file}.")

        elif db_type == "postgresql":
            command = ["pg_dump", "-U", config['user'], "-F", "c", "-b", "-v", "-f", output_file, db_name]
            subprocess.run(command, check=True)
            logger.info(f"PostgreSQL backup of {db_name} completed successfully, saved to {output_file}.")

        elif db_type == "mongodb":
            command = ["mongodump", "--db", db_name, "--out", output_file]
            subprocess.run(command, check=True)
            logger.info(f"MongoDB backup of {db_name} completed successfully, saved to {output_file}.")

        elif db_type == "sqlite":
            with open(output_file, 'w') as f:
                for line in config['conn'].iterdump():
                    f.write('%s\n' % line)
            logger.info(f"SQLite backup of {db_name} completed successfully, saved to {output_file}.")

        else:
            logger.error(f"Unsupported database type: {db_type}")
            raise ValueError(f"Unsupported database type: {db_type}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred during backup of {db_name} with {db_type}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during backup: {e}")
        raise

    return output_file
