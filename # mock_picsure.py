# mock_picsure.py
from dataclasses import dataclass, field
from typing import List, Dict, Any

# -----------------------------
# Mock classes to simulate PIC-SURE
# -----------------------------

@dataclass
class MockQuery:
    filters: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_filter(self, concept_path: str, operator: str, value: Any):
        self.filters.append({
            "concept_path": concept_path,
            "operator": operator,
            "value": value
        })
    
    def to_dict(self):
        return {"filters": self.filters}
    
    def get_results(self):
        # Mock result dataset
        mock_data = [
            {"participant_id": 1, "gender": "Male", "age": 55, "conditions": ["Type 2 Diabetes"]},
            {"participant_id": 2, "gender": "Female", "age": 60, "conditions": ["Hypertension"]},
            {"participant_id": 3, "gender": "Male", "age": 45, "conditions": ["Type 2 Diabetes", "Hypertension"]},
        ]
        # Apply simple filter simulation
        results = []
        for record in mock_data:
            match = True
            for f in self.filters:
                path = f["concept_path"]
                op = f["operator"]
                val = f["value"]
                # Only handle simple equality for demo
                if path == "demographics.gender" and not record["gender"] == val:
                    match = False
                if path == "conditions.name" and val not in record["conditions"]:
                    match = False
            if match:
                results.append(record)
        return results

@dataclass
class MockSession:
    api_url: str = ""
    token: str = ""
    
    def build_query(self):
        return MockQuery()


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    # Initialize session (mock)
    session = MockSession(api_url="https://mock-picsure.org", token="FAKE_TOKEN")
    
    # Build query
    query = session.build_query()
    query.add_filter("demographics.gender", "=", "Male")
    query.add_filter("conditions.name", "=", "Type 2 Diabetes")
    
    # Inspect query structure
    print("Query structure:")
    print(query.to_dict())
    
    # Fetch mock results
    results = query.get_results()
    print("\nQuery results:")
    for r in results:
        print(r)
