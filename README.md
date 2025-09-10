# ATM Controller

A simple ATM controller implementation that handles the core logic of ATM operations without UI or hardware dependencies. Designed for easy integration with real bank systems and hardware in the future.

## Features

- **Card Insertion & PIN Verification**
- **Account Selection**
- **Balance Inquiry**
- **Cash Withdrawal**
- **Cash Deposit**
- **State Management**
- **Extensible Architecture**
- **Comprehensive Test Suite**

## Project Structure


## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Installation

1. **Clone or create the project files**:

```bash
# Create project directory
mkdir atm-controller
cd atm-controller
```
2. **Set up a virtual environment**:
### Create virtual environment
python -m venv venv

### Activate on Windows
venv\Scripts\activate

### Activate on macOS/Linux
source venv/bin/activate

# Running the code
## Method 1: Run the Test Suite
```bash
python test_atm.py
```
This will execute all test cases and show you the ATM workflow in action.

## Method 2: Run Interactive Demo
```bash
python demo.py
```

## Method 3: Import and Use in your code.
```bash
from atm_controller import ATMController, MockBankSystem, MockHardware

# Initialize
bank_system = MockBankSystem()
hardware = MockHardware()
atm = ATMController(bank_system, hardware)

# Use the ATM
atm.insert_card("1234567890")
atm.enter_pin("1234")
accounts = atm.get_available_accounts()
atm.select_account("1001")
balance = atm.check_balance()
success, new_balance = atm.withdraw(100)
atm.eject_card()
```


