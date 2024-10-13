import tarfile
import os

def compress_backup(backup_file, output_file, logger):
    """
    Compress a backup file into a tar.gz archive.

    :param backup_file: The path to the backup file to compress
    :param output_file: The path where the compressed file will be saved
    :param logger: Logger instance for logging compression operations
    """
    try:
        # Check if the backup file exists before attempting to compress
        if not os.path.isfile(backup_file):
            logger.error(f"Backup file '{backup_file}' does not exist.")
            raise FileNotFoundError(f"Backup file '{backup_file}' does not exist.")
        
        with tarfile.open(output_file, "w:gz") as tar:
            tar.add(backup_file, arcname=os.path.basename(backup_file))
        
        logger.info(f"Backup compressed successfully to '{output_file}'.")

    except tarfile.TarError as e:
        logger.error(f"Error while compressing backup file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during compression: {e}")
        raise
