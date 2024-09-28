# ATM-Machine-Simulation

This ATM Machine Simulator is a Python-based desktop application built using the Tkinter library. It simulates common ATM functionalities such as withdrawing cash, depositing money, viewing transaction history, and managing account settings. The application supports user authentication with login and registration features, as well as a simple graphical user interface for interaction.

## Features

	•	User Registration and Login: Users can create accounts with a username and PIN, and securely log in to access their accounts.
	•	Cash Withdrawal: Users can withdraw a specified amount from their account balance after verifying their PIN.
	•	Deposit Money: Users can deposit money into their account.
	•	Transaction History: The application logs all transactions and allows users to view their transaction history.
	•	Quick Cash: A one-click option to withdraw ₹500 quickly.
	•	Account Settings: Users can update their account details, such as username and PIN.
	•	Logout: Users can log out securely to return to the login screen.
	•	Credit Card Placeholder: A placeholder feature for future credit card functionality.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/atm-simulator.git
   ```

2. Navigate to the project directory:

   ```bash
   cd atm-simulator
   ```

3. Ensure that Python is installed on your system. Install the required libraries if needed:

   ```bash
   pip install tkinter
   ```

4. Run the application:

   ```bash
   python atm_simulator.py
   ```

## Usage

- Upon starting the application, users will be greeted with a login screen.
- New users can register by entering a username and a PIN.
- Existing users can log in to access their accounts and perform transactions.
- The application supports operations like cash withdrawal, deposit, and quick cash withdrawal.
- Transaction history and account settings are accessible via the main screen.
- The application automatically saves user data using the `pickle` module.

## Data Persistence

User data (username, PIN, balance, and transactions) is stored locally using Python's **pickle** module. The data is saved in the `users.pkl` file and is loaded when the application starts.

## Future Improvements

- **Credit Card Functionality**: Currently, a placeholder exists for credit card-related features.
- **Enhanced Security**: Future updates may include encryption for sensitive data like PINs.
