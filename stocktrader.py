from app import create_app, db
from app.models import User, Stock, News, History, News_Settings

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Stock': Stock, 
        'News': News, 
        'History': History,
        'News_Settings': News_Settings
    }
