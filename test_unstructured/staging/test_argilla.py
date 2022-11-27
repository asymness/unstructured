import pytest

import argilla as rg
import unstructured.staging.argilla as argilla
from unstructured.documents.elements import Title, NarrativeText


@pytest.fixture
def elements():
    return [Title(text="example"), NarrativeText(text="another example")]


@pytest.fixture
def valid_metadata():
    return [{"score": 0.1}, {"category": "paragraph"}]


@pytest.fixture
def metadata_with_id():
    return [{"score": 0.1}, {"id": 1, "category": "paragraph"}]


@pytest.fixture
def metadata_with_invalid_length():
    return [{"score": 0.1}, {"category": "paragraph"}, {"type": "text"}]


@pytest.mark.parametrize(
    "task_name, dataset_type, extra_kwargs",
    [
        (
            "text_classification",
            rg.DatasetForTextClassification,
            {"metadata": [{"type": "text1"}, {"type": "text2"}]},
        ),
        (
            "text_classification",
            rg.DatasetForTextClassification,
            {},
        ),
    ],
)
def test_stage_for_argilla(elements, task_name, dataset_type, extra_kwargs):
    argilla_dataset = argilla.stage_for_argilla(elements, task_name, **extra_kwargs)
    assert isinstance(argilla_dataset, dataset_type)
    for record, element in zip(argilla_dataset, elements):
        assert record.text == element.text
        assert record.id == element.id
        for kwarg in extra_kwargs:
            assert getattr(record, kwarg) in extra_kwargs[kwarg]


@pytest.mark.parametrize(
    "task_name, error, error_message, extra_kwargs",
    [
        ("unkonwn_task", ValueError, "invalid value", {}),
        ("token_classification", NotImplementedError, None, {}),
        ("text2text", NotImplementedError, None, {}),
        ("text_classification", ValueError, "invalid value", {"metadata": "invalid metadata"}),
    ],
)
def test_invalid_stage_for_argilla(elements, task_name, error, error_message, extra_kwargs):
    with pytest.raises(error) as e:
        argilla.stage_for_argilla(elements, task_name, **extra_kwargs)
        assert error_message in e.args[0].lower() if error_message else True
