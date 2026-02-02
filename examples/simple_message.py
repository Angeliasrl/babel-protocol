#!/usr/bin/env python3
"""
BABEL Protocol - Simple Message Example

Demonstrates basic message creation, validation, and processing.
"""

from BABEL_COMPLETE_V1 import BABEL_MESSAGE, BABEL1
import json
from datetime import datetime

def create_simple_message():
    """Create a basic BABEL message"""
    message = BABEL_MESSAGE(
        from_agent="sensor_001",
        to_agent="control_hub",
        action="ASSERT",
        content={
            "sensor_type": "temperature",
            "value": 22.5,
            "unit": "celsius",
            "location": "Room A"
        },
        axioms_applied=["Σ1", "Θ1"],  # Integrity + Temporal causality
        timestamp=datetime.utcnow().isoformat() + "Z",
        human_readable="Temperature sensor reports 22.5°C in Room A"
    )
    
    return message

def validate_message(message):
    """Validate message structure and axioms"""
    print("=" * 60)
    print("BABEL MESSAGE VALIDATION")
    print("=" * 60)
    
    # Structural validation
    is_valid = BABEL1.validate_message(message)
    print(f"\n✓ Structure Valid: {is_valid}")
    
    # Axiom verification
    violations = BABEL1.verify_axioms(message)
    if not violations:
        print(f"✓ Axioms Valid: All axioms satisfied")
    else:
        print(f"✗ Axiom Violations: {violations}")
    
    return is_valid and not violations

def display_message(message):
    """Pretty print the message"""
    print("\n" + "=" * 60)
    print("MESSAGE CONTENT")
    print("=" * 60)
    print(json.dumps(message, indent=2, ensure_ascii=False))
    print()

def process_message(message):
    """Process the message content"""
    print("=" * 60)
    print("PROCESSING MESSAGE")
    print("=" * 60)
    
    action = message['action']
    content = message['content']
    from_agent = message['from']
    
    print(f"\nAction: {action}")
    print(f"From: {from_agent}")
    print(f"Human Readable: {message['human_readable']}")
    
    if action == "ASSERT":
        print(f"\nAssertion received:")
        print(f"  - Sensor Type: {content['sensor_type']}")
        print(f"  - Value: {content['value']} {content['unit']}")
        print(f"  - Location: {content['location']}")
        
        # Take action based on value
        if content['value'] > 25:
            print(f"\n⚠️  ALERT: Temperature exceeds threshold!")
        else:
            print(f"\n✓ Temperature within normal range")

def main():
    """Main execution"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "BABEL Protocol Demo" + " " * 24 + "║")
    print("║" + " " * 12 + "Simple Message Example" + " " * 23 + "║")
    print("╚" + "═" * 58 + "╝\n")
    
    # Create message
    print("Step 1: Creating BABEL message...")
    message = create_simple_message()
    
    # Display message
    print("\nStep 2: Displaying message structure...")
    display_message(message)
    
    # Validate message
    print("Step 3: Validating message...")
    is_valid = validate_message(message)
    
    if is_valid:
        # Process message
        print("\nStep 4: Processing message content...")
        process_message(message)
        
        print("\n" + "=" * 60)
        print("✓ MESSAGE PROCESSED SUCCESSFULLY")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗ MESSAGE VALIDATION FAILED")
        print("=" * 60)

if __name__ == "__main__":
    main()
