from app import create_app, db
import pymysql

def alter_cover_image_column():
    """Alter the cover_image column to TEXT type to handle longer URLs"""
    # Create app context
    app = create_app()
    
    with app.app_context():
        try:
            # Get database connection
            connection = db.engine.connect().connection
            cursor = connection.cursor()
            
            # Execute ALTER TABLE query
            cursor.execute("ALTER TABLE books MODIFY COLUMN cover_image TEXT;")
            
            # Commit the changes
            connection.commit()
            
            print("Database schema updated successfully!")
            print("The cover_image column has been changed from VARCHAR(255) to TEXT.")
            
        except Exception as e:
            print(f"Error updating database schema: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

if __name__ == "__main__":
    alter_cover_image_column() 