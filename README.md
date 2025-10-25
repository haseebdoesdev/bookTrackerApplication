# BookTracker Application

A Flask-based web application that allows users to manage their personal book collection, track reading progress, set reading challenges, and search for books using the Google Books API.

## Features

- **User Authentication**: Secure sign up and login using Flask-Login and bcrypt
- **Book Management**: Search for books with Google Books API or add books manually
- **Reading Progress Tracking**: Mark books as "Want to Read", "Currently Reading", or "Finished Reading"
- **Reading Challenges**: Set goals to read a specific number of books in a given timeframe
- **Book Reviews & Ratings**: Leave ratings and reviews with Markdown support
- **Search & Filtering**: Find books by title, author, category, rating, and reading status
- **Statistics**: View reading stats and visualize progress

## Technology Stack

- **Backend**: Flask, Python, SQLAlchemy
- **Database**: MySQL
- **Authentication**: Flask-Login, Flask-WTF, bcrypt
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript, Chart.js
- **API Integration**: Google Books API

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/bookTrackerApplication.git
cd bookTrackerApplication
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows:
   ```
   venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```
   source venv/bin/activate
   ```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Set up the MySQL database:
   - Create a new MySQL database named `book_tracker`
   - Update the database connection URI in the `.env` file

6. Configure environment variables:
   - Rename `.env.example` to `.env` (or create a new `.env` file)
   - Update the values in the `.env` file:
     ```
     SECRET_KEY=your_secret_key_here
     SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost/book_tracker
     GOOGLE_BOOKS_API_KEY=your_google_books_api_key
     ```

7. Get a Google Books API key:
   - Visit the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Books API
   - Create credentials for an API key
   - Add the API key to your `.env` file

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
```
python run.py
```
3. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

1. **Registration/Login**:
   - Create an account by signing up with a username, email, and password
   - Log in with your credentials

2. **Finding Books**:
   - Search for books using the search bar
   - Browse search results and add books to your library
   - Alternatively, add books manually if not found in the API

3. **Managing Your Library**:
   - View all your books in the library page
   - Filter books by status, category, or rating
   - Update reading progress for books you're currently reading

4. **Creating Challenges**:
   - Set reading goals with the challenge feature
   - Add completed books to your challenges
   - Track your progress toward achieving your reading goals

5. **Reviewing Books**:
   - Rate books on a scale of 1-5 stars
   - Write detailed reviews with Markdown formatting
   - View other users' reviews of books

6. **Viewing Statistics**:
   - Check your reading statistics in the profile section
   - View monthly reading activity
   - See your top rated books and recently finished books

## Screenshots

The `static/images/screenshots` directory contains screenshots of the application. If you'd like to see what the application looks like in action, please refer to these images.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Books API for book data
- Bootstrap 5 for the responsive UI
- Chart.js for statistics visualization 