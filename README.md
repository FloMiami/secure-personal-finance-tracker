# Secure Personal Finance Tracker

**A command-line application for tracking income and expenses with basic user authentication and data encryption for enhanced privacy.**

## Project Overview

This project, developed as a senior capstone, aims to provide a simple yet secure way for users to manage their personal finances through a command-line interface. It focuses on the fundamental aspects of financial tracking – recording income and expenses – while incorporating basic security measures to protect the confidentiality of user data. The application prioritizes ease of use within a text-based environment while demonstrating key concepts in data security and user management.

## Table of Contents

* [Key Features](#key-features)
* [Technologies Used](#technologies-used)
* [Implementation Details](#implementation-details)
    * [User Authentication](#user-authentication)
    * [Income and Expense Tracking](#income-and-expense-tracking)
    * [Basic Financial Reporting](#basic-financial-reporting)
    * [Data Encryption](#data-encryption)
* [Security Considerations (Important - For Review)](#security-considerations-important---for-review)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Running the Application](#running-the-application)
* [Usage](#usage)
    * [Creating an Account](#creating-an-account)
    * [Logging In](#logging-in)
    * [Adding Income](#adding-income)
    * [Adding Expenses](#adding-expenses)
    * [Viewing Transactions](#viewing-transactions)
    * [Viewing Balance](#viewing-balance)
    * [Exiting the Application](#exiting-the-application)
* [Future Enhancements](#future-enhancements)
* [Contributing](#contributing)
* [License](#license)
* [Author](#author)

## Key Features

* **User Authentication:** Secure access to financial data is controlled through a basic username and password login system.
* **Income and Expense Tracking:** Users can easily add new income sources and expense records, detailing the amount and a brief description. The application also allows viewing and deleting existing entries.
* **Basic Financial Reporting:** Provides a clear and concise summary of the user's financial health, displaying total income, total expenses, and the current balance.
* **Data Encryption:** Sensitive financial data stored locally is protected using the Fernet symmetric encryption library in Python, ensuring confidentiality at rest.
* **Local Data Storage:** Financial data is stored in plain text files (either CSV or JSON), offering a simple and portable storage solution.
* **Command-Line Interface:** A straightforward text-based interface makes the application accessible without requiring a graphical environment.

## Technologies Used

* **Python:** The core programming language used for all application logic and functionality.
* **CSV (Comma Separated Values):** One of the options for storing structured financial data locally.
* **JSON (JavaScript Object Notation):** The alternative option for storing structured financial data locally.
* **Cryptography Library (Fernet):** Used for implementing robust symmetric encryption for data security.
* **Standard Python Libraries:** Utilized for file operations, input/output, and basic data manipulation.

## Implementation Details

### User Authentication

The application implements a simple user authentication system where usernames and password hashes are stored (in a real-world scenario, securely in a database). Upon login, the entered password is hashed and compared against the stored hash. **For the version submitted on GitHub, actual password hashes have been removed for security reasons.**

### Income and Expense Tracking

Users can input income and expense records by providing a description and an amount. This data is then appended to the chosen local storage file (CSV or JSON) along with a timestamp. The application includes functions to view all recorded transactions and to delete specific entries based on their index.

### Basic Financial Reporting

The reporting feature calculates the total income and total expenses by reading and processing the data from the local storage file. The current balance is then derived by subtracting the total expenses from the total income. This summary is displayed to the user upon request.

### Data Encryption

Before saving any financial data to the local file, the application encrypts the entire content using the Fernet library. When the application starts or when data needs to be loaded, the file content is decrypted first. This ensures that even if the local storage file is accessed by an unauthorized party, the data remains unreadable without the correct encryption key.

## Security Considerations (Important - For Review)

This project incorporates basic security features as a demonstration of security principles. It is crucial to understand the limitations of this approach:

* **Password Storage:** For the version submitted on GitHub, actual password hashes in `users.json` have been replaced with placeholders. In a production environment, a dedicated and secure database with proper indexing and access controls would be essential.
* **Encryption Key Management:** The encryption key is currently handled within the application's scope. In a real-world scenario, secure key management practices, such as storing keys in dedicated secure storage or using key management services, are critical.
* **Command-Line Interface Security:** Command-line applications can be susceptible to certain types of attacks. Input validation and sanitization are important considerations for more robust applications.

This project serves as a foundational example of integrating security into a basic application. Further development would require a more comprehensive and industry-standard approach to security.

## Getting Started

### Prerequisites

* **Python 3.x:** Ensure that you have Python 3 or a later version installed on your system. You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).
* **Cryptography Library:** Install the `cryptography` library if you haven't already. You can install it using pip:

    ```bash
    pip install cryptography
    ```

### Running the Application

1.  **Clone or Download the Repository:** If you have the project files in a Git repository (e.g., on GitHub), clone it to your local machine. Otherwise, download the ZIP file and extract its contents.
2.  **Navigate to the Project Directory:** Open your terminal or command prompt and navigate to the directory containing the main Python script (e.g., `main.py` or `tracker.py`).
3.  **Run the Script:** Execute the application by running the Python script:

    ```bash
    python main.py  # Replace 'main.py' with the actual filename
    ```

    or

    ```bash
    python tracker.py # Replace 'tracker.py' with the actual filename
    ```

## Usage

Upon running the application, you will be presented with a menu of options:

### Creating an Account

If you are a new user, select the option to create an account. You will be prompted to enter a username and password. The password will be hashed before being (simulated as) stored.

### Logging In

If you have an existing account, select the login option and enter your username and password.

### Adding Income

Choose the option to add income. You will be asked to provide a description of the income source and the amount received.

### Adding Expenses

Select the option to add an expense. You will be prompted to enter a description of the expense and the amount spent.

### Viewing Transactions

Select the option to view all recorded income and expense entries, displayed with their descriptions and amounts.

### Viewing Balance

Choose the option to view your current financial balance, which is calculated based on your recorded income and expenses.

### Exiting the Application

Select the exit option to close the personal finance tracker. Your data will be saved (and encrypted) upon exiting.

## Future Enhancements

This project can be expanded with several features, including:

* **More Robust User Management:** Implement features like password reset, account deletion, and more secure password storage.
* **Categorization of Transactions:** Allow users to categorize income and expenses for better analysis.
* **More Advanced Reporting:** Generate charts and detailed reports on spending patterns over time.
* **Data Persistence Options:** Implement support for different data storage mechanisms, such as databases.
* **Error Handling and Input Validation:** Improve the application's robustness by adding more comprehensive error handling and input validation.
* **User Interface Improvements:** Explore the possibility of a more user-friendly graphical interface.

## Contributing

Contributions to this project are welcome. If you have suggestions for improvements or find any issues, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

\MIT License

## Author

\Alexandro Soto
