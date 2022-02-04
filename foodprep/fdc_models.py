import enum

from attrs import Factory, define

__all__ = [
    "FDCFoodClassType",
    "FDCFoodItemModel",
    "FDCFoodNutrientModel",
    "FDCFoodPortionModel",
    "FDCMeasureUnitModel",
    "FDCNutrientModel",
]


@enum.unique
class FDCFoodClassType(enum.Enum):
    branded = "Branded"
    final = "FinalFood"
    survey = "Survey"


@define
class FDCMeasureUnitModel:
    name: str
    abbreviation: str


@define
class FDCNutrientModel:
    number: float
    unit_name: str
    name: str
    rank: int | None = None


@define
class FDCFoodPortionModel:
    measure_unit: FDCMeasureUnitModel
    gram_weight: int
    modifier: str | None = None
    portion_description: str | None = None


@define
class FDCFoodNutrientModel:
    nutrient: FDCNutrientModel
    amount: float


@define
class FDCFoodItemModel:
    food_class: FDCFoodClassType
    description: str
    food_nutrients: list[FDCFoodNutrientModel]
    fdc_id: int
    publication_date: str
    food_portions: list[FDCFoodPortionModel] = Factory(list)
