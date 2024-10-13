import argparse
import json
import logging
import os
from backup import db_connect, backup, restore, compression, storage, notify

def setup_logging(log_file):
    """
    Set up logging configuration. Logs to the specified file.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info(f"Logging initialized. Log file: {log_file}")
    
def validate_cloud_credentials(config, cloud_provider):
    """
    Validate that the necessary credentials are present for the specified cloud provider.
    """
    if cloud_provider == 's3':
        if not config.get('aws', {}).get('access_key') or not config.get('aws', {}).get('secret_key'):
            raise ValueError("AWS credentials are missing in the config.json.")
    elif cloud_provider == 'gcs':
        if not config.get('gcs', {}).get('service_account_key'):
            raise ValueError("Google Cloud Service Account key is missing in the config.json.")
    elif cloud_provider == 'azure':
        if not config.get('azure', {}).get('connection_string'):
            raise ValueError("Azure connection string is missing in the config.json.")

def main():
    parser = argparse.ArgumentParser(description="Database Backup CLI Tool")
    
    # Main arguments
    parser.add_argument('operation', choices=['backup', 'restore'], help="Operation to perform: backup or restore")
    
    # Database connection args
    parser.add_argument('--db-type', required=True,choices=["mysql", "postgresql", "mongodb", "sqlite"], help="Database type (mysql, postgresql, mongodb, sqlite)")
    parser.add_argument('--config', required=True, help="Path to JSON configuration file for database connection")
    
    # Backup args
    parser.add_argument('--output', help="Output backup file path")
    parser.add_argument('--compress', action='store_true', help="Compress the backup")
    
    # Restore args
    parser.add_argument('--backup-file', help="Backup file to restore")
    
    # Storage args
    parser.add_argument('--cloud', choices=['s3', 'gcs', 'azure'], help="Cloud storage option")
    parser.add_argument('--bucket', help="Cloud storage bucket name")
    
    # Slack notification via webhook
    parser.add_argument('--slack-webhook', help="Slack webhook URL for notifications")
    
    # Log file argument
    parser.add_argument('--log-file', help="Path to the log file", default='backup.log')
    
    # Parse the arguments
    args = parser.parse_args()

    # Set up logging with custom or default log file
    setup_logging(args.log_file)
    
    # Log start of the operation
    logging.info(f"Starting {args.operation} operation.")

    # Load database configuration from JSON file
    try:
        with open(args.config, 'r') as config_file:
            config = json.load(config_file)
            db_config = config['database']
    except Exception as e:
        logging.error(f"Failed to read config file: {e}")
        print(f"Failed to read config file: {e}")
        return
    
    # Ensure all required db_config fields are present
    required_keys = ['host', 'port', 'user', 'password', 'database']
    if not all(key in db_config for key in required_keys):
        logging.error("Config file is missing required database configuration keys.")
        print("Config file is missing required database configuration keys.")
        return
    
    # Validate cloud credentials if a cloud provider is specified
    if args.cloud:
        try:
            validate_cloud_credentials(db_config, args.cloud)
        except ValueError as e:
            logging.error(str(e))
            print(str(e))
            return
    try:
        # Operation: Backup
        if args.operation == 'backup':
            conn = db_connect.connect_to_db(args.db_type, db_config)
            if conn:
                logging.info(f"Successfully connected to {args.db_type} database.")
                backup_file = backup.full_backup(args.db_type, db_config['database'], db_config, args.output, logging)
                logging.info(f"Backup created at {args.output}.")
                
                if args.compress:
                    compression.compress_backup(backup_file, args.output + ".tar.gz", logger=logging)
                    logging.info(f"Backup compressed to {args.output}.tar.gz")
                
                if args.cloud:
                    storage.upload_to_cloud(args.cloud, args.output, args.bucket,config, logger=logging)
                    logging.info(f"Backup uploaded to {args.cloud} bucket {args.bucket}.")
                
                if "slack_webhook" in config and config["slack_webhook"]:
                    notify.send_slack_notification(config["slack_webhook"], "Backup completed successfully", logger=logging)
                    logging.info("Slack notification sent.")
            else:
                logging.error(f"Failed to connect to {args.db_type} database.")
        
        # Operation: Restore
        elif args.operation == 'restore':
            if not args.backup_file:
                logging.error("Error: --backup-file is required for restore operations.")
                print("Error: --backup-file is required for restore operations.")
                return
            
            restore.restore_backup(args.db_type, args.backup_file, db_config, logger=logging)
            logging.info(f"Database restored from {args.backup_file}.")
            
            if "slack_webhook" in config and config["slack_webhook"]:
                notify.send_slack_notification(config["slack_webhook"], "Restore operation completed successfully", logger=logging)
                logging.info("Slack notification sent.")
    
    except Exception as e:
        logging.error(f"An error occurred during the {args.operation} operation: {e}")
        print(f"An error occurred: {e}")
    
    # Log the end of the operation
    logging.info(f"{args.operation.capitalize()} operation completed.")

if __name__ == '__main__':
    main()
