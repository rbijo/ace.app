import pytest
from app.models.topic import Topic


def test_topic_node_creation():
    topic = Topic(
        subject_id=1,
        title="Introduction to Data Structures",
        description="Core concepts of memory and nodes",
        position_x=100.0,
        position_y=50.0,
        prerequisites=[10]
    )
    assert topic.title == "Introduction to Data Structures"
    assert topic.position_x == 100.0
    assert topic.position_y == 50.0
    assert topic.prerequisites == [10]
    assert topic.status == "not_started"

