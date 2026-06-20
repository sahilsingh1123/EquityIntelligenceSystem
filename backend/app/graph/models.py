from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    node_id: str
    node_type: str
    name: str
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    edge_id: str
    source_node: str
    target_node: str
    relationship: str
    weight: float = 1.0
