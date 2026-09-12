import pytest
from app.schemas.learning import FlowNode, FlowEdge, RoadmapResponse


def test_roadmap_flowchart_schema():
    node1 = FlowNode(id="1", label="Topic 1", status="completed", position_x=0.0, position_y=0.0)
    node2 = FlowNode(id="2", label="Topic 2", status="not_started", position_x=250.0, position_y=0.0)
    edge = FlowEdge(id="e-1-2", source="1", target="2")

    roadmap = RoadmapResponse(
        subject_id=10,
        subject_title="Computer Science 101",
        percentage_complete=50.0,
        nodes=[node1, node2],
        edges=[edge],
        next_recommended_topics=[]
    )

    assert roadmap.subject_id == 10
    assert roadmap.percentage_complete == 50.0
    assert len(roadmap.nodes) == 2
    assert len(roadmap.edges) == 1
    assert roadmap.edges[0].source == "1"

