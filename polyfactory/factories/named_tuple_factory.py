from polyfactory.factories.base import BaseFactory
from polyfactory.field_meta import FieldMeta, Null

from inspect import get_annotations, isclass

from typing import Any, Generic, TypeGuard, TypeVar

NamedTupleT = TypeVar("NamedTupleT", bound=tuple)


class NamedTupleFactory(Generic[NamedTupleT], BaseFactory[NamedTupleT]):
    """NamedTuple base factory"""

    __is_base_factory__ = True

    @classmethod
    def is_supported_type(cls, value: Any) -> TypeGuard[type[NamedTupleT]]:
        if isclass(value):
            return issubclass(value, tuple) and hasattr(value, "__annotations__")
        else:
            return False

    @classmethod
    def get_model_fields(cls) -> list[FieldMeta]:

        annotations = get_annotations(cls.__model__)

        result = [
            FieldMeta.from_type(
                annotation=annotation,
                name=name,
                default=cls.__model__._field_defaults.get(name, Null),
            )
            for name, annotation in annotations.items()
        ]

        return result
