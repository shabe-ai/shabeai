#!/usr/bin/env python3
"""Initialize the database with the new UUID schema."""

from app.database import init_db


def main():
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    print("All tables created with String(36) UUID columns.")


if __name__ == "__main__":
    main()
