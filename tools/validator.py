#!/usr/bin/env python3
"""
BABEL Protocol - Message Validator Tool

Command-line tool to validate BABEL messages from files or stdin.

Usage:
    python validator.py message.json
    echo '{"from":"alice",...}' | python validator.py --stdin
    python validator.py --batch messages/
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List
from BABEL_COMPLETE_V1 import BABEL1, BABEL_MESSAGE

class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text: str, color: str):
    """Print colored text"""
    print(f"{color}{text}{Colors.RESET}")

def validate_message_file(filepath: Path, verbose: bool = False) -> bool:
    """Validate a single message file"""
    try:
        with open(filepath, 'r') as f:
            message = json.load(f)
    except json.JSONDecodeError as e:
        print_colored(f"✗ {filepath}: Invalid JSON - {e}", Colors.RED)
        return False
    except Exception as e:
        print_colored(f"✗ {filepath}: Error reading file - {e}", Colors.RED)
        return False
    
    return validate_message(message, str(filepath), verbose)

def validate_message(message: Dict, source: str = "stdin", verbose: bool = False) -> bool:
    """Validate a single message"""
    
    # Structural validation
    try:
        is_valid = BABEL1.validate_message(message)
    except Exception as e:
        print_colored(f"✗ {source}: Validation error - {e}", Colors.RED)
        return False
    
    if not is_valid:
        print_colored(f"✗ {source}: Invalid message structure", Colors.RED)
        if verbose:
            print(f"   Missing or invalid fields")
        return False
    
    # Axiom verification
    try:
        violations = BABEL1.verify_axioms(message)
    except Exception as e:
        print_colored(f"⚠ {source}: Axiom verification error - {e}", Colors.YELLOW)
        violations = [str(e)]
    
    if violations:
        print_colored(f"⚠ {source}: Axiom violations detected", Colors.YELLOW)
        if verbose:
            for violation in violations:
                print(f"   - {violation}")
        return False
    
    # Success
    print_colored(f"✓ {source}: Valid BABEL message", Colors.GREEN)
    
    if verbose:
        print(f"   From: {message.get('from', 'unknown')}")
        print(f"   To: {message.get('to', 'unknown')}")
        print(f"   Action: {message.get('action', 'unknown')}")
        print(f"   Axioms: {', '.join(message.get('axioms_applied', []))}")
        print(f"   Human: {message.get('human_readable', 'N/A')}")
    
    return True

def validate_batch(directory: Path, verbose: bool = False) -> Dict[str, int]:
    """Validate all JSON files in directory"""
    results = {"total": 0, "valid": 0, "invalid": 0}
    
    json_files = list(directory.glob("*.json"))
    
    if not json_files:
        print_colored(f"⚠ No JSON files found in {directory}", Colors.YELLOW)
        return results
    
    print(f"\nValidating {len(json_files)} files...\n")
    
    for filepath in json_files:
        results["total"] += 1
        if validate_message_file(filepath, verbose):
            results["valid"] += 1
        else:
            results["invalid"] += 1
    
    return results

def print_summary(results: Dict[str, int]):
    """Print validation summary"""
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Total files: {results['total']}")
    print_colored(f"Valid: {results['valid']}", Colors.GREEN)
    
    if results['invalid'] > 0:
        print_colored(f"Invalid: {results['invalid']}", Colors.RED)
    else:
        print(f"Invalid: {results['invalid']}")
    
    success_rate = (results['valid'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(
        description='BABEL Protocol Message Validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Validate single file:
    python validator.py message.json
  
  Validate from stdin:
    echo '{"from":"alice",...}' | python validator.py --stdin
  
  Validate directory:
    python validator.py --batch messages/
  
  Verbose output:
    python validator.py message.json -v
        """
    )
    
    parser.add_argument('path', nargs='?', help='Path to message file or directory')
    parser.add_argument('--stdin', action='store_true', help='Read message from stdin')
    parser.add_argument('--batch', action='store_true', help='Validate all JSON files in directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Header
    print(f"\n{Colors.BOLD}BABEL Protocol Validator v1.0{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * 50}{Colors.RESET}\n")
    
    try:
        if args.stdin:
            # Read from stdin
            message_text = sys.stdin.read()
            try:
                message = json.loads(message_text)
            except json.JSONDecodeError as e:
                print_colored(f"✗ Invalid JSON from stdin: {e}", Colors.RED)
                sys.exit(1)
            
            success = validate_message(message, "stdin", args.verbose)
            sys.exit(0 if success else 1)
        
        elif args.path:
            path = Path(args.path)
            
            if not path.exists():
                print_colored(f"✗ Path not found: {path}", Colors.RED)
                sys.exit(1)
            
            if path.is_file():
                # Single file
                success = validate_message_file(path, args.verbose)
                sys.exit(0 if success else 1)
            
            elif path.is_dir():
                # Batch validation
                results = validate_batch(path, args.verbose)
                print_summary(results)
                sys.exit(0 if results['invalid'] == 0 else 1)
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        print_colored("\n\nValidation cancelled by user", Colors.YELLOW)
        sys.exit(130)
    except Exception as e:
        print_colored(f"\n✗ Unexpected error: {e}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
