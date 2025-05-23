# activity_logger.py
#
# This module provides the ActivityLogger class, a singleton for logging user activities to the database.
# It is used for auditing, tracking, and monitoring user actions in the inventory management system.
#
# Usage: Instantiated as a singleton (ActivityLogger()), used by UI and managers to log actions.
#
# Helper modules: Uses DatabaseManager for DB access, json for details serialization.

from core.database_manager import DatabaseManager
from datetime import datetime
import json

class ActivityLogger:
    """
    Singleton class for logging user activities to the user_logs table in the database.
    Used for audit trails, monitoring, and debugging.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ActivityLogger, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
            cls._instance._create_log_table()
        return cls._instance

    def _create_log_table(self):
        # Ensure the logs table exists (called on singleton init)
        try:
            query = """
            CREATE TABLE IF NOT EXISTS user_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp VARCHAR(30) NOT NULL,
                user_id INT,
                username VARCHAR(50),
                role VARCHAR(20),
                action VARCHAR(100) NOT NULL,
                target VARCHAR(255),
                details TEXT
            )
            """
            self.db_manager.execute_query(query)
        except Exception as e:
            print(f"Error creating logs table: {e}")

    def log_activity(self, user_info, action, target="", details=None):
        """
        Log user activity to the database.
        Args:
            user_info (dict): User info (id, username, role)
            action (str): Action performed
            target (str): Entity affected (optional)
            details (dict): Extra details (optional)
        Returns: True if successful, False otherwise
        """
        try:
            details_json = json.dumps(details) if details else None
            query = """
            INSERT INTO user_logs (timestamp, user_id, username, role, action, target, details)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            timestamp = datetime.now().isoformat()
            user_id = user_info.get('id') if user_info else None
            username = user_info.get('username') if user_info else 'Unknown'
            role = user_info.get('role') if user_info else 'Unknown'
            self.db_manager.execute_query(
                query, 
                (timestamp, user_id, username, role, action, target, details_json)
            )
            return True
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False
    
    def get_logs(self, limit=50, user_id=None, action_type=None):
        """
        Retrieve logs from the database with optional filtering.
        Args:
            limit (int): Max logs to retrieve
            user_id (int): Filter by user ID (optional)
            action_type (str): Filter by action type (optional)
        Returns: List of log entries as dicts
        """
        try:
            query = "SELECT * FROM user_logs"
            params = []
            conditions = []
            if user_id:
                conditions.append("user_id = %s")
                params.append(user_id)
            if action_type:
                conditions.append("action LIKE %s")
                params.append(f"%{action_type}%")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            query += " ORDER BY timestamp DESC LIMIT %s"
            params.append(limit)
            result = self.db_manager.execute_query(query, tuple(params))
            logs = []
            for row in result:
                log_entry = {
                    'id': row[0],
                    'timestamp': row[1],
                    'user_id': row[2],
                    'username': row[3],
                    'role': row[4],
                    'action': row[5],
                    'target': row[6]
                }
                if row[7]:
                    try:
                        log_entry['details'] = json.loads(row[7])
                    except:
                        log_entry['details'] = row[7]
                logs.append(log_entry)
            return logs
        except Exception as e:
            print(f"Error retrieving logs: {e}")
            return []
            
    def clear_logs(self, days_to_keep=30):
        """
        Clear old logs, keeping only recent entries.
        Args:
            days_to_keep (int): Number of days of logs to keep
        Returns: True if successful, False otherwise
        """
        try:
            from datetime import datetime, timedelta
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
            query = "DELETE FROM user_logs WHERE timestamp < %s"
            self.db_manager.execute_query(query, (cutoff_date,))
            return True
        except Exception as e:
            print(f"Error clearing logs: {e}")
            return False 