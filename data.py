from dataclasses import dataclass

@dataclass
class EmailContext:
    """Context for email operations."""
    email_address: str = "dummy@example.com"
    password: str = "dummy_password"