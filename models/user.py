class User:
    def __init__(self, user_id, username, password_hash, role, email, is_active):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.email = email
        self.is_active = is_active

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}', active={self.is_active})>"