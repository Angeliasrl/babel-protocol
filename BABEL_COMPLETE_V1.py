#!/usr/bin/env python3
"""
BABEL Protocol v1.0.0
Universal Grammar for Secure AI-to-AI Communication

Copyright (c) 2026 Angelia srl SB
Licensed under MIT License

This implementation provides:
- BABEL-0: Grammar (19 Axioms)
- BABEL-1: Language (primitives, syntax, pragmatics)
- Message validation and verification
- Cryptographic signatures (placeholder for Dilithium)
"""

import hashlib
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

# ============================================================================
# BABEL-0: AXIOMS (Grammar)
# ============================================================================

class BABEL0:
    """BABEL-0 Grammar: 19 Universal Axioms"""
    
    # Meta-Axioms (Ω)
    OMEGA_1 = "Consistency: No contradictions permitted"
    OMEGA_2 = "Completeness: All valid states expressible"
    OMEGA_3 = "Decidability: Finite verification time"
    
    # Logical Axioms (Λ)
    LAMBDA_1 = "Identity: A = A"
    LAMBDA_2 = "Non-Contradiction: ¬(A ∧ ¬A)"
    LAMBDA_3 = "Excluded Middle: A ∨ ¬A"
    LAMBDA_4 = "Leibniz Equality: If A = B, then P(A) = P(B)"
    
    # Structural Axioms (Σ)
    SIGMA_1 = "Referential Integrity: All references must resolve"
    SIGMA_2 = "Uniqueness: Identifiers are unique within scope"
    SIGMA_3 = "Completeness: Required fields must be present"
    SIGMA_4 = "Type Safety: Values match declared types"
    SIGMA_5 = "Hash Integrity: Content matches SHA-256"
    SIGMA_6 = "Completeness Chain: All dependencies included"
    SIGMA_7 = "Merkle Chain: Cryptographic chain of custody"
    
    # Semantic Axioms (Θ)
    THETA_1 = "Temporal Causality: Effects follow causes"
    THETA_2 = "Conservation: Derived values preserve totals"
    THETA_3 = "Derived Coherence: Computed fields consistent"
    THETA_4 = "Monotonicity: Sequences preserve order"
    THETA_5 = "State Consistency: Updates maintain invariants"
    THETA_6 = "Semantic Preservation: Meaning maintained across transformations"
    
    @classmethod
    def get_axiom_description(cls, axiom_id: str) -> str:
        """Get description for axiom ID"""
        axiom_map = {
            "Ω1": cls.OMEGA_1, "Ω2": cls.OMEGA_2, "Ω3": cls.OMEGA_3,
            "Λ1": cls.LAMBDA_1, "Λ2": cls.LAMBDA_2, "Λ3": cls.LAMBDA_3, "Λ4": cls.LAMBDA_4,
            "Σ1": cls.SIGMA_1, "Σ2": cls.SIGMA_2, "Σ3": cls.SIGMA_3, "Σ4": cls.SIGMA_4,
            "Σ5": cls.SIGMA_5, "Σ6": cls.SIGMA_6, "Σ7": cls.SIGMA_7,
            "Θ1": cls.THETA_1, "Θ2": cls.THETA_2, "Θ3": cls.THETA_3, "Θ4": cls.THETA_4,
            "Θ5": cls.THETA_5, "Θ6": cls.THETA_6
        }
        return axiom_map.get(axiom_id, "Unknown axiom")

# ============================================================================
# BABEL-1: LANGUAGE
# ============================================================================

class BABEL1:
    """BABEL-1 Language: Message structure and validation"""
    
    # Linguistic Acts (Pragmatics)
    LINGUISTIC_ACTS = {
        "ASSERT": "State a fact or claim",
        "QUERY": "Request information",
        "COMMAND": "Issue an instruction",
        "DECLARE": "Make a declaration",
        "PROMISE": "Commit to future action",
        "PERMIT": "Grant permission",
        "FORBID": "Deny permission"
    }
    
    @classmethod
    def validate_message(cls, message: Dict[str, Any]) -> bool:
        """Validate BABEL message structure"""
        
        # Required fields
        required = ["from", "to", "action", "content", "axioms_applied", "human_readable"]
        for field in required:
            if field not in message:
                return False
        
        # Action must be valid
        if message["action"] not in cls.LINGUISTIC_ACTS:
            return False
        
        # Axioms must be non-empty list
        if not isinstance(message["axioms_applied"], list) or len(message["axioms_applied"]) == 0:
            return False
        
        # Content must be dict
        if not isinstance(message["content"], dict):
            return False
        
        return True
    
    @classmethod
    def verify_axioms(cls, message: Dict[str, Any]) -> List[str]:
        """Verify axioms are satisfied (basic checks)"""
        violations = []
        
        axioms = message.get("axioms_applied", [])
        content = message.get("content", {})
        
        # Σ1: Referential Integrity
        if "Σ1" in axioms:
            if "in_reply_to" in message:
                if not message["in_reply_to"]:
                    violations.append("Σ1: Empty reference in in_reply_to")
        
        # Σ2: Uniqueness
        if "Σ2" in axioms:
            if "message_id" in message:
                # In real implementation, check against registry
                pass
        
        # Σ3: Completeness
        if "Σ3" in axioms:
            if not content:
                violations.append("Σ3: Content is empty")
        
        # Θ1: Temporal Causality
        if "Θ1" in axioms:
            if "timestamp" in message:
                try:
                    datetime.fromisoformat(message["timestamp"].replace("Z", "+00:00"))
                except:
                    violations.append("Θ1: Invalid timestamp format")
        
        # Θ2: Conservation
        if "Θ2" in axioms:
            # Example: Check if totals are preserved
            if "total" in content and "items" in content:
                computed_total = sum(item.get("amount", 0) for item in content.get("items", []))
                if abs(computed_total - content.get("total", 0)) > 0.01:
                    violations.append("Θ2: Total does not match sum of items")
        
        return violations

# ============================================================================
# MESSAGE CONSTRUCTOR
# ============================================================================

def BABEL_MESSAGE(
    from_agent: str,
    to_agent: str,
    action: str,
    content: Dict[str, Any],
    axioms_applied: List[str],
    human_readable: str,
    timestamp: Optional[str] = None,
    in_reply_to: Optional[str] = None,
    signature: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a BABEL-compliant message
    
    Args:
        from_agent: Sender identifier
        to_agent: Recipient identifier
        action: Linguistic act (ASSERT, QUERY, etc.)
        content: Message payload
        axioms_applied: List of axiom IDs that apply
        human_readable: Plain language description
        timestamp: ISO 8601 timestamp (auto-generated if None)
        in_reply_to: ID of message being replied to
        signature: Cryptographic signature
    
    Returns:
        BABEL message dictionary
    """
    message = {
        "message_id": str(uuid.uuid4()),
        "from": from_agent,
        "to": to_agent,
        "action": action,
        "content": content,
        "axioms_applied": axioms_applied,
        "timestamp": timestamp or datetime.utcnow().isoformat() + "Z",
        "human_readable": human_readable
    }
    
    if in_reply_to:
        message["in_reply_to"] = in_reply_to
    
    if signature:
        message["signature"] = signature
    
    return message

# ============================================================================
# CRYPTOGRAPHIC SIGNATURES (Placeholder for Dilithium)
# ============================================================================

def sign_message(message: Dict[str, Any], private_key: str) -> Dict[str, Any]:
    """
    Sign a BABEL message with Dilithium (placeholder implementation)
    
    In production, use actual Dilithium implementation from PQCrypto
    """
    # Create canonical representation
    canonical = json.dumps(message, sort_keys=True, ensure_ascii=False)
    
    # Placeholder: Use SHA-256 instead of Dilithium
    # TODO: Replace with actual Dilithium signature
    message_hash = hashlib.sha256(canonical.encode()).hexdigest()
    signature = f"DILITHIUM_PLACEHOLDER_{message_hash[:32]}"
    
    signed_message = message.copy()
    signed_message["signature"] = signature
    
    return signed_message

def verify_message(message: Dict[str, Any], public_key: str) -> bool:
    """
    Verify BABEL message signature (placeholder implementation)
    
    In production, use actual Dilithium verification from PQCrypto
    """
    if "signature" not in message:
        return False
    
    # Remove signature for verification
    message_copy = message.copy()
    claimed_signature = message_copy.pop("signature")
    
    # Recreate signature
    canonical = json.dumps(message_copy, sort_keys=True, ensure_ascii=False)
    message_hash = hashlib.sha256(canonical.encode()).hexdigest()
    expected_signature = f"DILITHIUM_PLACEHOLDER_{message_hash[:32]}"
    
    return claimed_signature == expected_signature

# ============================================================================
# VALIDATION ERRORS
# ============================================================================

class BABELValidationError(Exception):
    """Raised when message validation fails"""
    pass

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_message(message: Dict[str, Any], indent: int = 2) -> str:
    """Pretty-print a BABEL message"""
    return json.dumps(message, indent=indent, ensure_ascii=False)

def message_hash(message: Dict[str, Any]) -> str:
    """Compute SHA-256 hash of message"""
    canonical = json.dumps(message, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "BABEL0",
    "BABEL1",
    "BABEL_MESSAGE",
    "sign_message",
    "verify_message",
    "BABELValidationError",
    "format_message",
    "message_hash"
]

# ============================================================================
# MODULE INFO
# ============================================================================

__version__ = "1.0.0"
__author__ = "Francesco Riva / Angelia srl SB"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2026 Angelia srl SB"

if __name__ == "__main__":
    print(f"BABEL Protocol v{__version__}")
    print(f"Copyright {__copyright__}")
    print(f"Licensed under {__license__}")
    print("\nUse: from BABEL_COMPLETE_V1 import *")
