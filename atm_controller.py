from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

class TransactionType(Enum):
    BALANCE_INQUIRY = "balance_inquiry"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"

class ATMState(Enum):
    IDLE = "idle"
    CARD_INSERTED = "card_inserted"
    PIN_VERIFIED = "pin_verified"
    ACCOUNT_SELECTED = "account_selected"
    TRANSACTION_COMPLETED = "transaction_completed"

class BankSystemInterface(ABC):
    """Interface for bank system integration"""
    
    @abstractmethod
    def verify_pin(self, card_number: str, pin: str) -> bool:
        """Verify if the PIN is correct for the given card"""
        pass
    
    @abstractmethod
    def get_accounts(self, card_number: str) -> List[Dict]:
        """Get list of accounts for the given card"""
        pass
    
    @abstractmethod
    def get_balance(self, account_number: str) -> int:
        """Get current balance for the account"""
        pass
    
    @abstractmethod
    def withdraw(self, account_number: str, amount: int) -> bool:
        """Withdraw amount from account, returns success status"""
        pass
    
    @abstractmethod
    def deposit(self, account_number: str, amount: int) -> bool:
        """Deposit amount to account, returns success status"""
        pass

class HardwareInterface(ABC):
    """Interface for ATM hardware integration"""
    
    @abstractmethod
    def read_card(self) -> Optional[str]:
        """Read card number from card reader"""
        pass
    
    @abstractmethod
    def eject_card(self) -> bool:
        """Eject card from card reader"""
        pass
    
    @abstractmethod
    def dispense_cash(self, amount: int) -> bool:
        """Dispense cash from cash bin"""
        pass
    
    @abstractmethod
    def accept_cash(self) -> int:
        """Accept cash deposit, returns amount accepted"""
        pass

class MockBankSystem(BankSystemInterface):
    """Mock implementation of bank system for testing"""
    
    def __init__(self):
        self.accounts = {
            "1234567890": {  # card number
                "pin": "1234",
                "accounts": [
                    {"number": "1001", "name": "Checking", "balance": 1000},
                    {"number": "1002", "name": "Savings", "balance": 5000}
                ]
            },
            "0987654321": {
                "pin": "4321",
                "accounts": [
                    {"number": "2001", "name": "Checking", "balance": 2500}
                ]
            }
        }
    
    def verify_pin(self, card_number: str, pin: str) -> bool:
        if card_number in self.accounts:
            return self.accounts[card_number]["pin"] == pin
        return False
    
    def get_accounts(self, card_number: str) -> List[Dict]:
        if card_number in self.accounts:
            return self.accounts[card_number]["accounts"]
        return []
    
    def get_balance(self, account_number: str) -> int:
        for card_data in self.accounts.values():
            for account in card_data["accounts"]:
                if account["number"] == account_number:
                    return account["balance"]
        return 0
    
    def withdraw(self, account_number: str, amount: int) -> bool:
        if amount <= 0:
            return False
            
        for card_data in self.accounts.values():
            for account in card_data["accounts"]:
                if account["number"] == account_number:
                    if account["balance"] >= amount:
                        account["balance"] -= amount
                        return True
        return False
    
    def deposit(self, account_number: str, amount: int) -> bool:
        if amount <= 0:
            return False
            
        for card_data in self.accounts.values():
            for account in card_data["accounts"]:
                if account["number"] == account_number:
                    account["balance"] += amount
                    return True
        return False

class MockHardware(HardwareInterface):
    """Mock implementation of ATM hardware for testing"""
    
    def __init__(self):
        self.card_inserted = False
        self.card_number = None
    
    def read_card(self) -> Optional[str]:
        return self.card_number if self.card_inserted else None
    
    def eject_card(self) -> bool:
        # Always return True for testing purposes
        # In real hardware, this would check if card is actually inserted
        self.card_inserted = False
        self.card_number = None
        return True
    
    def dispense_cash(self, amount: int) -> bool:
        # Simulate cash dispensing
        return amount > 0
    
    def accept_cash(self) -> int:
        # Simulate accepting $100 for testing
        return 100

class ATMController:
    """Main ATM controller that handles the ATM workflow"""
    
    def __init__(self, bank_system: BankSystemInterface, hardware: HardwareInterface):
        self.bank_system = bank_system
        self.hardware = hardware
        self.state = ATMState.IDLE
        self.current_card = None
        self.selected_account = None
        self.transaction_history = []
    
    def insert_card(self, card_number: str) -> bool:
        """Simulate card insertion"""
        if self.state != ATMState.IDLE:
            return False
        
        self.current_card = card_number
        self.state = ATMState.CARD_INSERTED
        return True
    
    def enter_pin(self, pin: str) -> bool:
        """Verify PIN number"""
        if self.state != ATMState.CARD_INSERTED or not self.current_card:
            return False
        
        if self.bank_system.verify_pin(self.current_card, pin):
            self.state = ATMState.PIN_VERIFIED
            return True
        return False
    
    def get_available_accounts(self) -> List[Dict]:
        """Get list of available accounts for current card"""
        if self.state != ATMState.PIN_VERIFIED or not self.current_card:
            return []
        
        return self.bank_system.get_accounts(self.current_card)
    
    def select_account(self, account_number: str) -> bool:
        """Select an account for transactions"""
        if self.state != ATMState.PIN_VERIFIED:
            return False
        
        accounts = self.get_available_accounts()
        for account in accounts:
            if account["number"] == account_number:
                self.selected_account = account_number
                self.state = ATMState.ACCOUNT_SELECTED
                return True
        return False
    
    def check_balance(self) -> Optional[int]:
        """Check balance of selected account"""
        if self.state != ATMState.ACCOUNT_SELECTED or not self.selected_account:
            return None
        
        balance = self.bank_system.get_balance(self.selected_account)
        self.transaction_history.append({
            "type": TransactionType.BALANCE_INQUIRY,
            "account": self.selected_account,
            "amount": 0,
            "success": True
        })
        return balance
    
    def withdraw(self, amount: int) -> Tuple[bool, Optional[int]]:
        """Withdraw money from selected account"""
        if self.state != ATMState.ACCOUNT_SELECTED or not self.selected_account:
            return False, None
        
        if amount <= 0:
            return False, None
        
        success = self.bank_system.withdraw(self.selected_account, amount)
        if success:
            # Try to dispense cash
            cash_success = self.hardware.dispense_cash(amount)
            if not cash_success:
                # Reverse the transaction if cash dispensing fails
                self.bank_system.deposit(self.selected_account, amount)
                success = False
        
        self.transaction_history.append({
            "type": TransactionType.WITHDRAWAL,
            "account": self.selected_account,
            "amount": amount,
            "success": success
        })
        
        if success:
            new_balance = self.bank_system.get_balance(self.selected_account)
            return True, new_balance
        return False, None
    
    def deposit(self, amount: int) -> Tuple[bool, Optional[int]]:
        """Deposit money to selected account"""
        if self.state != ATMState.ACCOUNT_SELECTED or not self.selected_account:
            return False, None
        
        if amount <= 0:
            return False, None
        
        # Accept cash from hardware
        accepted_amount = self.hardware.accept_cash()
        if accepted_amount != amount:
            # For simplicity, we'll use the accepted amount
            amount = accepted_amount
        
        success = self.bank_system.deposit(self.selected_account, amount)
        
        self.transaction_history.append({
            "type": TransactionType.DEPOSIT,
            "account": self.selected_account,
            "amount": amount,
            "success": success
        })
        
        if success:
            new_balance = self.bank_system.get_balance(self.selected_account)
            return True, new_balance
        return False, None
    
    def eject_card(self) -> bool:
        """Eject card and reset state"""
        success = self.hardware.eject_card()
        if success:
            self._reset_state()
        return success
    
    def cancel_transaction(self) -> bool:
        """Cancel current transaction and eject card"""
        return self.eject_card()
    
    def _reset_state(self):
        """Reset controller state"""
        self.state = ATMState.IDLE
        self.current_card = None
        self.selected_account = None