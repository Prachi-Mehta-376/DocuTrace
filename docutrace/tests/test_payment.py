import pytest
from src.payment.payment_service import (
    validate_card, calculate_fee, save_transaction, PaymentService, _transactions
)

def test_validate_card_happy_path():
    """Test validate_card with a valid 16-digit card number."""
    assert validate_card("1234567812345678") is True

def test_validate_card_invalid_length():
    """Test validate_card with an invalid length card number."""
    assert validate_card("12345") is False

def test_calculate_fee_happy_path():
    """Test calculate_fee with a standard amount."""
    assert calculate_fee(100.0) == 2.0

def test_calculate_fee_zero():
    """Test calculate_fee with zero amount."""
    assert calculate_fee(0.0) == 0.0

def test_save_transaction_happy_path():
    """Test save_transaction appends a transaction to the list."""
    initial_len = len(_transactions)
    save_transaction({"id": 1, "status": "success"})
    assert len(_transactions) == initial_len + 1
    assert _transactions[-1]["id"] == 1

def test_save_transaction_empty():
    """Test save_transaction with an empty dictionary."""
    initial_len = len(_transactions)
    save_transaction({})
    assert len(_transactions) == initial_len + 1
    assert _transactions[-1] == {}

def test_payment_service_process_happy_path():
    """Test PaymentService.process with valid inputs."""
    service = PaymentService()
    result = service.process("1111222233334444", 200.0)
    assert result["amount"] == 200.0
    assert result["fee"] == 4.0
    assert result["total_amount"] == 204.0
    assert result["status"] == "success"
    assert result["card_number"] == "****4444"

def test_payment_service_process_invalid_card():
    """Test PaymentService.process with invalid card number raises ValueError."""
    service = PaymentService()
    with pytest.raises(ValueError, match="Invalid card number format"):
        service.process("invalid_card", 100.0)
