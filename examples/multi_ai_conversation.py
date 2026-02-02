#!/usr/bin/env python3
"""
BABEL Protocol - Multi-AI Conversation Example

Demonstrates a conversation between multiple AI agents using BABEL,
including queries, responses, consensus, and conflict resolution.
"""

from BABEL_COMPLETE_V1 import BABEL_MESSAGE, BABEL1
import json
from datetime import datetime
from typing import List, Dict

class AIAgent:
    """Simple AI agent that speaks BABEL"""
    
    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
        self.inbox = []
        self.conversation_history = []
    
    def send_message(self, to_agent: str, action: str, content: Dict, 
                     axioms: List[str], human_text: str, in_reply_to=None):
        """Send a BABEL message"""
        message = BABEL_MESSAGE(
            from_agent=self.agent_id,
            to_agent=to_agent,
            action=action,
            content=content,
            axioms_applied=axioms,
            timestamp=datetime.utcnow().isoformat() + "Z",
            human_readable=human_text,
            in_reply_to=in_reply_to
        )
        
        # Validate before sending
        if not BABEL1.validate_message(message):
            raise ValueError("Invalid message structure")
        
        self.conversation_history.append(("SENT", message))
        return message
    
    def receive_message(self, message: Dict):
        """Receive and validate a BABEL message"""
        # Validate incoming message
        if not BABEL1.validate_message(message):
            print(f"⚠️  {self.agent_id}: Rejected invalid message")
            return False
        
        # Check axioms
        violations = BABEL1.verify_axioms(message)
        if violations:
            print(f"⚠️  {self.agent_id}: Rejected message with axiom violations: {violations}")
            return False
        
        self.inbox.append(message)
        self.conversation_history.append(("RECEIVED", message))
        return True

def print_message(agent: AIAgent, direction: str, message: Dict):
    """Pretty print a message"""
    arrow = "→" if direction == "SENT" else "←"
    print(f"\n{arrow} {agent.agent_id} ({direction})")
    print(f"   Action: {message['action']}")
    print(f"   To/From: {message['to'] if direction == 'SENT' else message['from']}")
    print(f"   Human: {message['human_readable']}")
    print(f"   Axioms: {', '.join(message['axioms_applied'])}")

def scenario_1_simple_query():
    """Scenario 1: Simple query-response"""
    print("\n" + "═" * 70)
    print("SCENARIO 1: Simple Query-Response")
    print("═" * 70)
    
    # Create agents
    alice = AIAgent("alice", "weather_monitor")
    bob = AIAgent("bob", "data_provider")
    
    # Alice queries Bob
    query = alice.send_message(
        to_agent="bob",
        action="QUERY",
        content={"question": "What is the current temperature?"},
        axioms=["Σ1"],
        human_text="Alice requests current temperature"
    )
    print_message(alice, "SENT", query)
    
    # Bob receives query
    bob.receive_message(query)
    print_message(bob, "RECEIVED", query)
    
    # Bob responds
    response = bob.send_message(
        to_agent="alice",
        action="ASSERT",
        content={"temperature": 22.5, "unit": "celsius", "timestamp": query['timestamp']},
        axioms=["Σ1", "Θ1"],
        human_text="Bob reports temperature of 22.5°C",
        in_reply_to=query.get('message_id')
    )
    print_message(bob, "SENT", response)
    
    # Alice receives response
    alice.receive_message(response)
    print_message(alice, "RECEIVED", response)
    
    print("\n✓ Scenario 1 completed successfully")

def scenario_2_multi_party_consensus():
    """Scenario 2: Multi-party consensus building"""
    print("\n" + "═" * 70)
    print("SCENARIO 2: Multi-Party Consensus")
    print("═" * 70)
    
    # Create agents
    coordinator = AIAgent("coordinator", "system_admin")
    agent_a = AIAgent("agent_a", "worker")
    agent_b = AIAgent("agent_b", "worker")
    agent_c = AIAgent("agent_c", "worker")
    
    # Coordinator proposes action
    proposal = coordinator.send_message(
        to_agent="ALL_WORKERS",
        action="DECLARE",
        content={"proposal": "upgrade_system", "scheduled_time": "2026-02-03T03:00:00Z"},
        axioms=["Σ1", "Θ1"],
        human_text="Coordinator proposes system upgrade at 3 AM tomorrow"
    )
    print_message(coordinator, "SENT", proposal)
    
    # Workers receive proposal
    for agent in [agent_a, agent_b, agent_c]:
        agent.receive_message(proposal)
        print_message(agent, "RECEIVED", proposal)
    
    # Workers vote
    votes = []
    for agent in [agent_a, agent_b, agent_c]:
        vote = agent.send_message(
            to_agent="coordinator",
            action="PERMIT",
            content={"vote": "approve", "reason": "System ready for upgrade"},
            axioms=["Σ1"],
            human_text=f"{agent.agent_id} approves the upgrade proposal",
            in_reply_to=proposal.get('message_id')
        )
        print_message(agent, "SENT", vote)
        votes.append(vote)
    
    # Coordinator receives votes
    for vote in votes:
        coordinator.receive_message(vote)
        print_message(coordinator, "RECEIVED", vote)
    
    # Coordinator confirms consensus
    confirmation = coordinator.send_message(
        to_agent="ALL_WORKERS",
        action="DECLARE",
        content={"status": "consensus_reached", "action": "upgrade_scheduled"},
        axioms=["Σ1", "Θ1"],
        human_text="Consensus reached: upgrade will proceed as scheduled"
    )
    print_message(coordinator, "SENT", confirmation)
    
    print("\n✓ Scenario 2 completed: Consensus achieved")

def scenario_3_conflict_detection():
    """Scenario 3: Detecting and handling conflicts"""
    print("\n" + "═" * 70)
    print("SCENARIO 3: Conflict Detection")
    print("═" * 70)
    
    # Create agents
    sensor_1 = AIAgent("sensor_1", "temperature_sensor")
    sensor_2 = AIAgent("sensor_2", "temperature_sensor")
    validator = AIAgent("validator", "data_validator")
    
    # Both sensors report different temperatures for same location
    report_1 = sensor_1.send_message(
        to_agent="validator",
        action="ASSERT",
        content={"location": "Room A", "temperature": 22.5, "unit": "celsius"},
        axioms=["Σ1", "Θ1"],
        human_text="Sensor 1 reports 22.5°C in Room A"
    )
    print_message(sensor_1, "SENT", report_1)
    
    report_2 = sensor_2.send_message(
        to_agent="validator",
        action="ASSERT",
        content={"location": "Room A", "temperature": 25.8, "unit": "celsius"},
        axioms=["Σ1", "Θ1"],
        human_text="Sensor 2 reports 25.8°C in Room A"
    )
    print_message(sensor_2, "SENT", report_2)
    
    # Validator receives both
    validator.receive_message(report_1)
    validator.receive_message(report_2)
    print_message(validator, "RECEIVED", report_1)
    print_message(validator, "RECEIVED", report_2)
    
    # Validator detects conflict
    print(f"\n⚠️  CONFLICT DETECTED:")
    print(f"   Location: Room A")
    print(f"   Sensor 1: {report_1['content']['temperature']}°C")
    print(f"   Sensor 2: {report_2['content']['temperature']}°C")
    print(f"   Difference: {abs(report_1['content']['temperature'] - report_2['content']['temperature'])}°C")
    
    # Validator requests clarification
    clarification_request = validator.send_message(
        to_agent="ALL_SENSORS",
        action="QUERY",
        content={
            "question": "Conflicting readings detected. Please verify calibration.",
            "location": "Room A"
        },
        axioms=["Σ1", "Θ1"],
        human_text="Validator requests sensor calibration verification"
    )
    print_message(validator, "SENT", clarification_request)
    
    print("\n✓ Scenario 3 completed: Conflict detected and handled")

def main():
    """Run all scenarios"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "BABEL Protocol Demo" + " " * 29 + "║")
    print("║" + " " * 15 + "Multi-AI Conversation Example" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    
    try:
        scenario_1_simple_query()
        scenario_2_multi_party_consensus()
        scenario_3_conflict_detection()
        
        print("\n" + "═" * 70)
        print("✓ ALL SCENARIOS COMPLETED SUCCESSFULLY")
        print("═" * 70)
        print("\nKey Takeaways:")
        print("  • BABEL enables structured, verifiable AI-to-AI communication")
        print("  • Messages are validated before processing (security)")
        print("  • Conflicts can be detected through axiom verification")
        print("  • Multi-party consensus is straightforward to implement")
        print()
        
    except Exception as e:
        print(f"\n✗ Error during execution: {e}")
        raise

if __name__ == "__main__":
    main()
