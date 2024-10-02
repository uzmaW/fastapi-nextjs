from sqlmodel import SQLModel, Field, Session, create_engine
from sqlalchemy.orm import sessionmaker
from .models.user import User
from sqlalchemy import event
from sqlalchemy import text
from passlib.context import CryptContext
from ..config.mt_config import MtConfig as mt_config

# Create the database engine
engine = create_engine(mt_config.SQLALCHEMY_DATABASE_URI)

# Create a sessionmaker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# get crypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DATABASE_URL = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}"

def getDatabaseUrl():
    """Get the database URL from the mt_config."""
    return DATABASE_URL.format(
                            POSTGRES_USER=mt_config.POSTGRES_USER,
                            POSTGRES_PASSWORD=mt_config.POSTGRES_PASSWORD,
                            POSTGRES_HOST=mt_config.POSTGRES_HOST,  # Use the host from settings
                            POSTGRES_SERVER=mt_config.POSTGRES_SERVER,  # Use the server from settings
                            POSTGRES_PORT=mt_config.POSTGRES_PORT  # Use the port from settings) 
    )

def seed_tables(target, connection, **kw):
    """Seed the database with initial data if not already seeded."""
    # Check if the admin user already exists
    if connection.scalar(User.__table__.select().where(User.email == 'admin@example.com')):
        return
    
    # Insert the admin user
    connection.execute(User.__table__.insert(), [
        {
            'email': 'admin@example.com',
            'hashed_password': pwd_context.hash('admin123'),
            'is_superuser': True
        }
    ])
    


# Listen for the 'after_create' event to seed the tables
event.listen(User.__table__, 'after_create', seed_tables)

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables(engine):
    """Create all tables in the database."""
    SQLModel.metadata.create_all(bind=engine)

def drop_tables(engine):
    """Drop all tables in the database."""
    SQLModel.metadata.drop_all(bind=engine)

def setup_database(db: Session):
    """Setup the database by creating tables and seeding data."""
    try:
        database_url = getDatabaseUrl()
        engine = create_engine(database_url)

        with engine.connect() as conn:
            conn.execute(text("COMMIT"))
            db_exists = conn.execute(text(f"select from pg_database where datname = '{mt_config.POSTGRES_DB}'"))
            
            if db_exists.fetchone() is None:
                print(f"Database {mt_config.POSTGRES_DB} does not exist. Creating...")
                conn.execute(text(f"CREATE DATABASE {mt_config.POSTGRES_DB}"))
            
                conn.execute(text("COMMIT"))
                conn.close()
                
                """ recreate engine with database """
                engine = create_engine(mt_config.SQLALCHEMY_DATABASE_URI)
            
            create_tables(engine)
        # You can call seed_tables here if needed
    except Exception as e:
        print(f"Error setting up the database: {e}")