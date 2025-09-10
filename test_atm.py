from atm_controller import (
    MockBankSystem,
    MockHardware,
    ATMController
)

# Test cases
def test_atm_controller():
    """Test the ATM controller functionality"""
    
    # Setup
    bank_system = MockBankSystem()
    hardware = MockHardware()
    atm = ATMController(bank_system, hardware)
    
    # Test 1: Successful balance inquiry
    print("Test 1: Successful balance inquiry")
    assert atm.insert_card("1234567890")
    assert atm.enter_pin("1234")
    accounts = atm.get_available_accounts()
    assert len(accounts) == 2
    assert atm.select_account("1001")
    balance = atm.check_balance()
    assert balance == 1000
    assert atm.eject_card()
    print("✓ Test 1 passed\n")
    
    # Test 2: Successful withdrawal
    print("Test 2: Successful withdrawal")
    assert atm.insert_card("1234567890")
    assert atm.enter_pin("1234")
    assert atm.select_account("1001")
    success, new_balance = atm.withdraw(100)
    assert success
    assert new_balance == 900
    assert atm.eject_card()
    print("✓ Test 2 passed\n")
    
    # Test 3: Failed withdrawal (insufficient funds)
    print("Test 3: Failed withdrawal (insufficient funds)")
    assert atm.insert_card("1234567890")
    assert atm.enter_pin("1234")
    assert atm.select_account("1001")
    success, new_balance = atm.withdraw(2000)
    assert not success
    assert atm.eject_card()
    print("✓ Test 3 passed\n")
    
    # Test 4: Successful deposit
    print("Test 4: Successful deposit")
    assert atm.insert_card("1234567890")
    assert atm.enter_pin("1234")
    assert atm.select_account("1001")
    success, new_balance = atm.deposit(100)
    assert success
    # Balance should be back to 1000 (900 + 100)
    assert new_balance == 1000
    assert atm.eject_card()
    print("✓ Test 4 passed\n")
    
    # Test 5: Invalid PIN
    print("Test 5: Invalid PIN")
    assert atm.insert_card("1234567890")
    assert not atm.enter_pin("wrong")
    # Should still be able to eject card even with wrong PIN
    assert atm.eject_card()
    print("✓ Test 5 passed\n")
    
    # Test 6: Invalid card (simulate by trying operations without proper card)
    print("Test 6: Invalid operations without card")
    # Try to enter PIN without card
    assert not atm.enter_pin("1234")
    # Try to select account without card
    assert not atm.select_account("1001")
    print("✓ Test 6 passed\n")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_atm_controller()