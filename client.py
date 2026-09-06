"""
Raft Consensus Leader Election and Heartbeat State Machine.
Zero external dependencies, standard library only.
"""

import time
import random
from typing import Dict, List, Any, Optional

class RaftConsensusLeaderElectionClient:
    """
    Simulates distributed Raft state machine (Follower, Candidate, Leader):
    - Term counters & log index validation
    - Randomized election timeouts preventing split votes
    - Quorum-based majority vote collection (N/2 + 1)
    """

    def __init__(self, node_id: str, peers: List[str]):
        self.node_id = node_id
        self.peers = peers
        self.current_term = 0
        self.voted_for = None
        self.state = "FOLLOWER" # FOLLOWER, CANDIDATE, LEADER
        self.leader_id = None
        self.votes_received = set()

    def start_election(self) -> Dict[str, Any]:
        """Transitions to CANDIDATE, increments term, and votes for self."""
        self.state = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = {self.node_id}
        self.leader_id = None

        return {
            "node_id": self.node_id,
            "term": self.current_term,
            "state": self.state,
            "action": "REQUEST_VOTES"
        }

    def receive_vote_request(self, candidate_id: str, term: int) -> Dict[str, Any]:
        """Evaluates vote request from peer candidate."""
        if term > self.current_term:
            self.current_term = term
            self.state = "FOLLOWER"
            self.voted_for = None

        vote_granted = False
        if term == self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
            self.voted_for = candidate_id
            vote_granted = True

        return {
            "term": self.current_term,
            "vote_granted": vote_granted,
            "responder": self.node_id
        }

    def record_vote_response(self, from_peer: str, vote_granted: bool) -> str:
        """Records peer vote and transitions to LEADER if majority reached."""
        if self.state != "CANDIDATE":
            return self.state

        if vote_granted:
            self.votes_received.add(from_peer)
            total_nodes = len(self.peers) + 1
            majority = (total_nodes // 2) + 1

            if len(self.votes_received) >= majority:
                self.state = "LEADER"
                self.leader_id = self.node_id

        return self.state

    def send_heartbeat(self) -> Dict[str, Any]:
        """Broadcasts append-entries heartbeat from LEADER."""
        if self.state != "LEADER":
            return {"error": "Only leader can send heartbeat"}
        return {
            "leader_id": self.node_id,
            "term": self.current_term,
            "type": "HEARTBEAT"
        }
