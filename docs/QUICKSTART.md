# BABEL Protocol - Quick Start Guide

Get BABEL running in **5 minutes**.

---

## Installation

```bash
# Clone repository
git clone https://github.com/angelia/babel-protocol.git
cd babel-protocol

# Install dependencies
pip install pycryptodome
```

---

## Your First BABEL Message

### 1. Import the Protocol

```python
from BABEL_COMPLETE_V1 import BABEL_MESSAGE, BABEL1
```

### 2. Create a Message

```python
message = BABEL_MESSAGE(
    from_agent="weather_station",
    to_agent="control_center",
    action="ASSERT",
    content={
        "temperature": 22.5,
        "humidity": 65,
        "location": "Milan"
    },
    axioms_applied=["Σ1", "Θ1", "Θ2"],
    timestamp="2026-02-02T14:30:00Z",
    human_readable="Weather station reports current conditions"
)
```

### 3. Validate the Message

```python
# Structural validation
is_valid = BABEL1.validate_message(message)
print(f"Valid: {is_valid}")  # True

# Axiom verification
violations = BABEL1.verify_axioms(message)
print(f"Violations: {violations}")  # []
```

---

## Adding Cryptographic Signatures

### Generate Keys (First Time Only)

```python
from Crypto.PublicKey import ECC

# Generate Dilithium-equivalent keys (using ECC as placeholder)
key = ECC.generate(curve='Ed25519')
private_key = key.export_key(format='PEM')
public_key = key.public_key().export_key(format='PEM')

# Save keys securely
with open('private.pem', 'w') as f:
    f.write(private_key)
with open('public.pem', 'w') as f:
    f.write(public_key)
```

### Sign Messages

```python
from BABEL_COMPLETE_V1 import sign_message

# Load private key
with open('private.pem', 'r') as f:
    private_key = f.read()

# Sign message
signed_message = sign_message(message, private_key)
print(signed_message['signature'])  # Cryptographic signature
```

### Verify Signatures

```python
from BABEL_COMPLETE_V1 import verify_message

# Load public key
with open('public.pem', 'r') as f:
    public_key = f.read()

# Verify authenticity
is_authentic = verify_message(signed_message, public_key)
print(f"Authentic: {is_authentic}")  # True
```

---

## Receiving and Processing Messages

### Basic Receiver

```python
def process_babel_message(raw_message):
    """Process incoming BABEL message"""
    
    # 1. Validate structure
    if not BABEL1.validate_message(raw_message):
        raise ValueError("Invalid BABEL message structure")
    
    # 2. Verify signature (if present)
    if 'signature' in raw_message:
        if not verify_message(raw_message, sender_public_key):
            raise ValueError("Invalid signature")
    
    # 3. Check axioms
    violations = BABEL1.verify_axioms(raw_message)
    if violations:
        raise ValueError(f"Axiom violations: {violations}")
    
    # 4. Process content safely
    action = raw_message['action']
    content = raw_message['content']
    
    if action == "ASSERT":
        # Handle assertion
        return handle_assertion(content)
    elif action == "QUERY":
        # Handle query
        return handle_query(content)
    # ... other actions
```

---

## Integration Patterns

### Pattern 1: Request-Response

```python
# Agent A sends query
query = BABEL_MESSAGE(
    from_agent="agent_a",
    to_agent="agent_b",
    action="QUERY",
    content={"question": "What is the temperature?"},
    axioms_applied=["Σ1"],
    human_readable="Request for temperature data"
)

# Agent B responds
response = BABEL_MESSAGE(
    from_agent="agent_b",
    to_agent="agent_a",
    action="ASSERT",
    content={"answer": "22.5°C"},
    axioms_applied=["Σ1", "Θ1"],
    in_reply_to=query['message_id'],  # Link to original query
    human_readable="Temperature reading response"
)
```

### Pattern 2: Multi-Party Consensus

```python
# Agent A makes proposal
proposal = BABEL_MESSAGE(
    from_agent="agent_a",
    to_agent="ALL",
    action="DECLARE",
    content={"proposal": "System upgrade at 3 AM"},
    axioms_applied=["Σ1", "Θ1"],
    human_readable="Proposes system maintenance window"
)

# Agents B, C, D vote
vote_b = BABEL_MESSAGE(
    from_agent="agent_b",
    to_agent="agent_a",
    action="PERMIT",
    content={"vote": "approve"},
    axioms_applied=["Σ1"],
    in_reply_to=proposal['message_id'],
    human_readable="Approves maintenance proposal"
)
```

### Pattern 3: Command Execution

```python
# Authenticated command
command = BABEL_MESSAGE(
    from_agent="admin_agent",
    to_agent="worker_agent",
    action="COMMAND",
    content={"command": "backup_database"},
    axioms_applied=["Σ1", "Σ7", "Θ1"],
    signature="...",  # Cryptographically signed
    human_readable="Initiates database backup"
)

# Worker verifies then executes
if verify_message(command, admin_public_key):
    execute_command(command['content']['command'])
```

---

## Common Axiom Combinations

| Use Case | Axioms | Meaning |
|----------|--------|---------|
| Simple data exchange | `Σ1` | Integrity check only |
| Timestamped event | `Σ1, Θ1` | Integrity + temporal order |
| Financial transaction | `Σ1, Σ7, Θ2, Θ4` | Integrity + chain + conservation + monotonicity |
| Audit trail | `Σ1, Σ6, Σ7, Θ1` | Integrity + completeness + chain + causality |
| Critical command | `Σ1-Σ7, Θ1-Θ6` | All structural + semantic axioms |

---

## Error Handling

```python
from BABEL_COMPLETE_V1 import BABELValidationError

try:
    # Attempt to process message
    process_babel_message(incoming_message)
except BABELValidationError as e:
    # Structural violation
    log_error(f"Invalid message structure: {e}")
except ValueError as e:
    # Signature or axiom violation
    log_security_event(f"Security violation: {e}")
except Exception as e:
    # Unexpected error
    log_critical(f"Processing error: {e}")
```

---

## Performance Tips

### 1. Cache Public Keys
```python
# Don't reload from disk every time
public_keys = {}

def get_public_key(agent_id):
    if agent_id not in public_keys:
        public_keys[agent_id] = load_key_from_storage(agent_id)
    return public_keys[agent_id]
```

### 2. Batch Validation
```python
# Validate multiple messages at once
def validate_batch(messages):
    return [BABEL1.validate_message(m) for m in messages]
```

### 3. Skip Axiom Verification for Trusted Channels
```python
# For internal, encrypted channels
if is_internal_channel:
    # Only validate structure, skip axioms
    is_valid = BABEL1.validate_message(message)
else:
    # Full validation for external messages
    is_valid = BABEL1.validate_message(message)
    violations = BABEL1.verify_axioms(message)
```

---

## Next Steps

- **Production Deployment:** [`docs/DEPLOYMENT.md`](DEPLOYMENT.md)
- **Platform Integration:** [`docs/integrations/`](integrations/)
- **Advanced Examples:** [`examples/`](../examples/)
- **Full Specification:** [`SPECIFICATION.md`](SPECIFICATION.md)

---

## Troubleshooting

### "Message validation failed"
- Check that all required fields are present
- Verify field types match specification
- Ensure `axioms_applied` is a non-empty list

### "Signature verification failed"
- Confirm you're using the correct public key
- Check that message wasn't modified after signing
- Verify signature format (base64 encoded)

### "Axiom violations detected"
- Review which axioms are being violated
- Check if content matches declared axioms
- Ensure timestamps are in correct format (ISO 8601)

---

**Questions?** Open an issue on GitHub or contact francesco.riva@angelia.cloud
