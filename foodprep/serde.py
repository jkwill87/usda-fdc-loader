from typing import Type, TypeVar

from attrs import fields
from cattr import Converter, global_converter
from cattr.gen import make_dict_structure_fn, make_dict_unstructure_fn, override

from foodprep.dataset_models import NutritionModel
from foodprep.fdc_models import FDCFoodItemModel, FDCFoodPortionModel, FDCNutrientModel

converter: Converter = global_converter

_T = TypeVar("_T")


def lazy_cast(o: _T, t: Type[_T]) -> _T:
    return t(o) if o else t()


converter.register_structure_hook(float, lazy_cast)


def camel_to_snake(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


for fdc_class in {FDCNutrientModel, FDCFoodPortionModel, FDCFoodItemModel}:
    hook = make_dict_structure_fn(
        fdc_class,
        converter,
        **{a.name: override(rename=camel_to_snake(a.name)) for a in fields(fdc_class)},
    )
    converter.register_structure_hook(fdc_class, hook)  # type: ignore

converter.register_unstructure_hook(
    NutritionModel,
    make_dict_unstructure_fn(NutritionModel, converter, _cattrs_omit_if_default=True),
)
