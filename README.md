**User Transaction Report**
This project is a web application built using Dash and SQLite that provides an interactive report on user transactions. It includes features for data visualization and filtering based on user inputs.




Features
Date Range Picker: Filter data based on a date range.
User Selection: Select a specific user to view their transaction data.
Email Search: Search users by email.
Sorting Options: Sort the data by total spent or by user name.
Charts and Tables:
Bar chart displaying the top 3 spenders.
Line chart showing transaction amounts over time.
Table with user transaction report.
Table listing users with no transactions.
Installation
Clone the Repository

git clone <repository-url>
cd <repository-directory>
Create and Activate a Virtual Environment

# Install virtualenv if not already installed
pip install virtualenv

# Create a virtual environment
virtualenv myenv

# Activate the virtual environment
# Windows
myenv\Scripts\activate
# macOS and Linux
source myenv/bin/activate
Install Dependencies



pip install -r requirements.txt
Usage
Initialize the Database
Before running the application, ensure that the SQLite database is set up and seeded with data:



python initialize_db.py
Run the Application
To start the Dash web application:




python app.py
The application will be available at http://127.0.0.1:8050/ by default.
*/
 
 
