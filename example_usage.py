"""
Demonstration of genpark-raft-leader-election-heartbeat-consensus-skill
"""

from client import RaftConsensusLeaderElectionClient

def main():
    peers = ["agent_node_2", "agent_node_3", "agent_node_4", "agent_node_5"]
    node1 = RaftConsensusLeaderElectionClient("agent_node_1", peers)

    # 1. Timeout triggers election
    election = node1.start_election()
    print("=== STARTING RAFT ELECTION ===")
    print("Node State:", election)

    # 2. Collect votes from peers
    print("\nCollecting peer votes...")
    node1.record_vote_response("agent_node_2", vote_granted=True)
    print("Votes received (2/5), state:", node1.state)

    node1.record_vote_response("agent_node_3", vote_granted=True)
    print("Votes received (3/5 - Majority achieved!), state:", node1.state)

    # 3. Leader sends heartbeat
    hb = node1.send_heartbeat()
    print("\nLeader Heartbeat broadcast:", hb)

if __name__ == "__main__":
    main()
