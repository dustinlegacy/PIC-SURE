from dataclasses import dataclass, field
from typing import List, Dict, Any


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
        # Mock dataset
        mock_data = [
            {"participant_id": 1, "gender": "Male", "age": 55, "conditions": ["Type 2 Diabetes"]},
            {"participant_id": 2, "gender": "Female", "age": 60, "conditions": ["Hypertension"]},
            {"participant_id": 3, "gender": "Male", "age": 45, "conditions": ["Type 2 Diabetes", "Hypertension"]},
            {"participant_id": 4, "gender": "Female", "age": 35, "conditions": ["Asthma"]},
        ]
        
        results = []
        for record in mock_data:
            match = True
            for f in self.filters:
                path = f["concept_path"]
                op = f["operator"]
                val = f["value"]
                
                # Handle demographics.gender
                if path == "demographics.gender":
                    if op == "=" and record["gender"] != val:
                        match = False
                        
                # Handle conditions.name
                elif path == "conditions.name":
                    if op == "=" and val not in record["conditions"]:
                        match = False
                
                # Handle numeric filters (e.g., age)
                elif path == "age":
                    if op == "=" and record["age"] != val:
                        match = False
                    elif op == ">" and record["age"] <= val:
                        match = False
                    elif op == "<" and record["age"] >= val:
                        match = False
                    elif op == ">=" and record["age"] < val:
                        match = False
                    elif op == "<=" and record["age"] > val:
                        match = False
            
            if match:
                results.append(record)
        return results

@dataclass
class MockSession:
    api_url: str = ""
    token: str = ""
    
    def build_query(self):d
        return MockQuery()


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    session = MockSession()
    query = session.build_query()
    
    # Add multiple filters
    query.add_filter("demographics.gender", "=", "Male")
    query.add_filter("conditions.name", "=", "Type 2 Diabetes")
    query.add_filter("age", ">", 50)
    
    print("Query structure:")
    print(query.to_dict())
    
    results = query.get_results()
    print("\nQuery results:")
    for r in results:
        print(r)
