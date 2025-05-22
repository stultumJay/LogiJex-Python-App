from core.database_manager import DatabaseManager
from datetime import datetime
import json

class ActivityLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ActivityLogger, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
            cls._instance._create_log_table()
        return cls._instance

    def _create_log_table(self):
        # Ensure the logs table exists
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
        Log user activity to the database
        
        Args:
            user_info (dict): Dictionary containing user information (id, username, role)
            action (str): Description of the action performed
            target (str): The object/entity affected by the action (optional)
            details (dict): Additional details about the action (optional)
        """
        try:
            # Prepare the details as JSON string if provided
            details_json = json.dumps(details) if details else None
            
            # Insert log entry
            query = """
            INSERT INTO user_logs (timestamp, user_id, username, role, action, target, details)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Format current timestamp
            timestamp = datetime.now().isoformat()
            
            # Extract user info
            user_id = user_info.get('id') if user_info else None
            username = user_info.get('username') if user_info else 'Unknown'
            role = user_info.get('role') if user_info else 'Unknown'
            
            # Execute query
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
        Retrieve logs from the database with optional filtering
        
        Args:
            limit (int): Maximum number of logs to retrieve
            user_id (int): Filter logs by user ID (optional)
            action_type (str): Filter logs by action type (optional)
            
        Returns:
            list: List of log entries as dictionaries
        """
        try:
            # Start building the query
            query = "SELECT * FROM user_logs"
            params = []
            
            # Add filters if provided
            conditions = []
            if user_id:
                conditions.append("user_id = %s")
                params.append(user_id)
                
            if action_type:
                conditions.append("action LIKE %s")
                params.append(f"%{action_type}%")
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            # Add order by and limit
            query += " ORDER BY timestamp DESC LIMIT %s"
            params.append(limit)
            
            # Execute query
            result = self.db_manager.execute_query(query, tuple(params))
            
            # Process the results
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
                
                # Parse details if available
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
        Clear old logs, keeping only recent entries
        
        Args:
            days_to_keep (int): Number of days of logs to keep
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Calculate cutoff date
            from datetime import datetime, timedelta
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
            
            # Delete logs older than cutoff
            query = "DELETE FROM user_logs WHERE timestamp < %s"
            self.db_manager.execute_query(query, (cutoff_date,))
            
            return True
        except Exception as e:
            print(f"Error clearing logs: {e}")
            return False 