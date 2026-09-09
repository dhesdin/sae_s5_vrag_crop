import pytest

from v_crop_rag.models.vlm import BoundingBox, VisualElement

# valid cases
def test_create_bounding_box():
    bbox = BoundingBox(
        x_min=10,
        y_min=20,
        x_max=30,
        y_max=40
    )
    
    assert bbox.x_min == 10
    assert bbox.y_min == 20
    assert bbox.x_max == 30
    assert bbox.y_max == 40
    

def test_create_visual_element():
    bbox = BoundingBox(
        x_min=10,
        y_min=20,
        x_max=30,
        y_max=40
    )
    
    visual_element = VisualElement(
        label="Test Label",
        description="Test Description",
        attributes={"key1": "value1", "key2": "value2"},
        bbox=bbox
    )
    
    assert visual_element.label == "Test Label"
    assert visual_element.description == "Test Description"
    assert visual_element.attributes == {"key1": "value1", "key2": "value2"}
    assert visual_element.bbox == bbox
    

# defauult cases
def test_visual_element_default_bbox():
    visual_element = VisualElement(
        label="Test Label",
        description="Test Description"
    )
    
    assert visual_element.bbox is None


def test_visual_element_default_attributes():
    visual_element = VisualElement(
        label="Test Label",
        description="Test Description"
    )
    
    assert visual_element.attributes == {}


# missing required fields
def test_bouding_box_missing_fields():
    with pytest.raises(ValueError):
        BoundingBox(
            x_min=10,
            y_min=20,
            x_max=30
        )
        

def test_visual_element_missing_label():
    with pytest.raises(ValueError):
        VisualElement(
            description="Test Description"
        )


def test_visual_element_missing_description():
    with pytest.raises(ValueError):
        VisualElement(
            label="Test Label"
        )

