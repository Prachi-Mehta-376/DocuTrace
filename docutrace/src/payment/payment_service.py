_transactions = []

def validate_card(card_number: str) -> bool:
    """Validates if the card number format is correct (basic length and digit check)."""
    return len(card_number) == 16 and card_number.isdigit()

def calculate_fee(amount: float) -> float:
    """Calculates a simple processing fee of 2%."""
    return round(amount * 0.02, 2)

def save_transaction(transaction: dict) -> None:
    """Saves the transaction to an in-memory list."""
    _transactions.append(transaction)

class PaymentService:
    """A service for processing mock payments."""
    
    def process(self, card_number: str, amount: float) -> dict:
        """Processes a payment by validating, calculating fee, and saving the transaction."""
        if not validate_card(card_number):
            raise ValueError("Invalid card number format")
        
        fee = calculate_fee(amount)
        total_amount = amount + fee
        
        transaction = {
            "card_number": f"****{card_number[-4:]}",
            "amount": amount,
            "fee": fee,
            "total_amount": total_amount,
            "status": "success"
        }
        
        save_transaction(transaction)
        return transaction
