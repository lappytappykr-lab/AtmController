#!/usr/bin/env python3
"""
Simple demo script for the ATM Controller
"""

from atm_controller import ATMController, MockBankSystem, MockHardware

def run_demo():
    print("=== ATM Controller Demo ===\n")
    
    # Initialize the ATM system
    bank_system = MockBankSystem()
    hardware = MockHardware()
    atm = ATMController(bank_system, hardware)
    
    # Demo workflow
    print("1. Inserting card...")
    if atm.insert_card("1234567890"):
        print("   ✓ Card inserted successfully")
    else:
        print("   ✗ Failed to insert card")
        return
    
    print("\n2. Entering PIN...")
    if atm.enter_pin("1234"):
        print("   ✓ PIN verified successfully")
    else:
        print("   ✗ Invalid PIN")
        atm.eject_card()
        return
    
    print("\n3. Available accounts:")
    accounts = atm.get_available_accounts()
    for i, account in enumerate(accounts, 1):
        print(f"   {i}. {account['name']} ({account['number']})")
    
    print("\n4. Selecting Checking account...")
    if atm.select_account("1001"):
        print("   ✓ Account selected")
    else:
        print("   ✗ Failed to select account")
        atm.eject_card()
        return
    
    print("\n5. Checking balance...")
    balance = atm.check_balance()
    print(f"   ✓ Current balance: ${balance}")
    
    print("\n6. Withdrawing $100...")
    success, new_balance = atm.withdraw(100)
    if success:
        print(f"   ✓ Withdrawal successful. New balance: ${new_balance}")
    else:
        print("   ✗ Withdrawal failed")
    
    print("\n7. Depositing $50...")
    success, new_balance = atm.deposit(50)
    if success:
        print(f"   ✓ Deposit successful. New balance: ${new_balance}")
    else:
        print("   ✗ Deposit failed")
    
    print("\n8. Ejecting card...")
    if atm.eject_card():
        print("   ✓ Card ejected successfully")
    else:
        print("   ✗ Failed to eject card")
    
    print("\n=== Demo completed ===")

if __name__ == "__main__":
    run_demo()