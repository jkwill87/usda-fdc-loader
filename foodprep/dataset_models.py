from __future__ import annotations

import json
import re
from textwrap import dedent
from typing import Any, Iterable

from attr import Factory, asdict, define
from cattr import unstructure

from foodprep.fdc_models import (
    FDCFoodClassType,
    FDCFoodItemModel,
    FDCFoodNutrientModel,
    FDCFoodPortionModel,
)
from foodprep.utils import mdy_to_ymd


@define
class NutritionModel:
    # other
    energy_kcal: float = 0.0
    cholestorol_mg: float = 0.0

    # macronutrients
    protein_g: float = 0.0
    carbs_total_g: float = 0.0
    carbs_sugar_g: float = 0.0
    carbs_fibre_g: float = 0.0
    fat_total_g: float = 0.0
    fat_mono_g: float = 0.0
    fat_poly_g: float = 0.0
    fat_sat_g: float = 0.0
    fat_trans_g: float = 0.0

    # micronutrients
    calcium_mg: float = 0.0
    folate_ug: float = 0.0
    iron_mg: float = 0.0
    magnesium_mg: float = 0.0
    niacin_mg: float = 0.0
    potassium_mg: float = 0.0
    riboflavin_mg: float = 0.0
    selenium_ug: float = 0.0
    sodium_mg: float = 0.0
    thiamin_mg: float = 0.0
    vitamin_a_ug: float = 0.0
    vitamin_b12_ug: float = 0.0
    vitamin_b6_mg: float = 0.0
    vitamin_c_mg: float = 0.0
    vitamin_d_ug: float = 0.0
    vitamin_e_mg: float = 0.0
    zinc_mg: float = 0.0

    @classmethod
    def from_fdc_food_nutrients(
        cls, food_nutrients: Iterable[FDCFoodNutrientModel]
    ) -> NutritionModel:
        nutrition = cls()

        for food_nutrient in food_nutrients:
            amount = food_nutrient.amount
            match food_nutrient.nutrient.number:
                case 208 | 957 | 958:
                    nutrition.energy_kcal = max(nutrition.energy_kcal, amount)
                case 268:
                    nutrition.energy_kcal = max(nutrition.energy_kcal, amount / 4.1868)
                case 601:
                    nutrition.cholestorol_mg = amount
                case 203:
                    nutrition.protein_g = amount
                case 205 | 205.2 | 209:
                    nutrition.carbs_total_g = max(nutrition.carbs_total_g, amount)
                case 269 | 269.3:
                    nutrition.carbs_sugar_g = max(nutrition.carbs_sugar_g, amount)
                    nutrition.carbs_total_g = max(nutrition.carbs_total_g, amount)
                case 291 | 293 | 295 | 297:
                    nutrition.carbs_fibre_g = max(nutrition.carbs_fibre_g, amount)
                    nutrition.carbs_total_g = max(nutrition.carbs_total_g, amount)
                case 204 | 298:
                    nutrition.fat_total_g = max(nutrition.fat_total_g, amount)
                case 645:
                    nutrition.fat_mono_g = max(nutrition.fat_mono_g, amount)
                    nutrition.fat_total_g = max(nutrition.fat_total_g, amount)
                case 646:
                    nutrition.fat_poly_g = max(nutrition.fat_poly_g, amount)
                    nutrition.fat_total_g = max(nutrition.fat_total_g, amount)
                case 606:
                    nutrition.fat_sat_g = max(nutrition.fat_sat_g, amount)
                    nutrition.fat_total_g = max(nutrition.fat_total_g, amount)
                case 605 | 693 | 694 | 695:
                    nutrition.fat_trans_g = max(nutrition.fat_trans_g, amount)
                    nutrition.fat_total_g = max(nutrition.fat_total_g, amount)
                case 301:
                    nutrition.calcium_mg = amount
                case 417 | 432 | 435:
                    nutrition.folate_ug = max(nutrition.folate_ug, amount)
                case 303:
                    nutrition.iron_mg = amount
                case 304:
                    nutrition.magnesium_mg = amount
                case 406:
                    nutrition.niacin_mg = amount
                case 306:
                    nutrition.potassium_mg = amount
                case 405:
                    nutrition.riboflavin_mg = amount
                case 317:
                    nutrition.selenium_ug = amount
                case 307:
                    nutrition.sodium_mg = amount
                case 404:
                    nutrition.thiamin_mg = amount
                case 320:
                    nutrition.vitamin_a_ug = amount
                case 323 | 573:
                    nutrition.vitamin_e_mg = max(nutrition.vitamin_e_mg, amount)
                case 415:
                    nutrition.vitamin_b6_mg = amount
                case 418 | 578:
                    nutrition.vitamin_b12_ug = max(nutrition.vitamin_b12_ug, amount)
                case 401:
                    nutrition.vitamin_c_mg = amount
                case 328 | 325 | 326:
                    nutrition.vitamin_d_ug = max(nutrition.vitamin_d_ug, amount)
                case 324:
                    nutrition.vitamin_d_ug = max(nutrition.vitamin_d_ug, amount * 4.0)
                case 309:
                    nutrition.zinc_mg = amount

        if nutrition.energy_kcal == 0.0:
            nutrition.energy_kcal += nutrition.protein_g * 4.1868
            nutrition.energy_kcal += nutrition.carbs_total_g * 4.1868
            nutrition.energy_kcal += nutrition.fat_total_g * 9.097
        nutrition.energy_kcal = round(nutrition.energy_kcal, 3)
        return nutrition


@define
class PortionModel:
    title: str
    grams: float

    @classmethod
    def from_fdc_final(
        cls, portions: Iterable[FDCFoodPortionModel]
    ) -> Iterable[PortionModel]:
        banned_modifiers = {"dia", "NLEA"}
        for portion in portions:
            if not (title := portion.measure_unit.name):
                continue
            title = title.lower()
            if portion.modifier and all(
                bm not in portion.modifier for bm in banned_modifiers
            ):
                title = f"{title} ({portion.modifier.strip()})"
            title = title.replace("~", "approx ", 1)
            yield PortionModel(title, portion.gram_weight)

    @classmethod
    def from_fdc_survey(
        cls, portions: Iterable[FDCFoodPortionModel]
    ) -> Iterable[PortionModel]:
        for portion in portions:
            if not (title := portion.portion_description):
                continue
            if not portion.gram_weight:
                continue
            title = title.lower()
            if "not specified" in title:
                continue
            title = re.sub(r", ns (?:as|to) \w+", "", title)
            title = title.replace(", nfs", "", 1)
            title = title.replace("guideline amount per ", "", 1)
            title = title.replace(" dia", "", 1)
            yield PortionModel(title, portion.gram_weight)


@define
class IngredientModel:
    title: str
    fdc_id: int
    fdc_date: str
    nutrition: NutritionModel = NutritionModel()
    portions: list[PortionModel] = Factory(list)

    @classmethod
    def from_fdc_final(cls, food_item: FDCFoodItemModel) -> IngredientModel:
        title = food_item.description
        title = re.sub(r", with add(?:\w+) ingredients", "", title)
        title = re.sub(r"(\w+),(\w+)", r"\1, \2", title)
        portions = sorted(
            PortionModel.from_fdc_final(food_item.food_portions),
            key=lambda p: p.grams,
        )
        nutrition = NutritionModel.from_fdc_food_nutrients(food_item.food_nutrients)
        return cls(
            title=title,
            fdc_id=food_item.fdc_id,
            fdc_date=mdy_to_ymd(food_item.publication_date),
            portions=portions,
            nutrition=nutrition,
        )

    @classmethod
    def from_fdc_survey(cls, food_item: FDCFoodItemModel) -> IngredientModel:
        title = food_item.description
        title = re.sub(r", with add(?:\w+) ingredients", "", title)
        title = re.sub(r"(\w+),(\w+)", r"\1, \2", title)
        title = re.sub(r", NS (?:as|to) \w+", "", title)
        title = re.sub(r",? as ingredient.*", "", title)
        title = title.replace(", NFS", "", 1)
        title = title.replace("or NFS", "", 1)
        portions = sorted(
            PortionModel.from_fdc_survey(food_item.food_portions),
            key=lambda p: p.grams,
        )
        nutrition = NutritionModel.from_fdc_food_nutrients(food_item.food_nutrients)
        return cls(
            title=title,
            fdc_id=food_item.fdc_id,
            fdc_date=mdy_to_ymd(food_item.publication_date),
            portions=portions,
            nutrition=nutrition,
        )

    @classmethod
    def from_fdc_data(cls, food_item: FDCFoodItemModel) -> IngredientModel:
        match food_item.food_class:
            case FDCFoodClassType.final:
                return cls.from_fdc_final(food_item)
            case FDCFoodClassType.survey:
                return cls.from_fdc_survey(food_item)
            case FDCFoodClassType.branded:
                raise NotImplementedError

    def to_dict(self) -> dict[str, Any]:
        return unstructure(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict()) + "\n"

    def to_sqlite(self) -> str:
        stmts = []
        # ingredients entry
        stmts.append(
            """\
            INSERT INTO ingredients (fdc_id, fdc_date, title)
            VALUES ({fdc_id}, '{fdc_date}', '{title}');
            """.format(
                fdc_id=self.fdc_id,
                fdc_date=self.fdc_date,
                title=self.title.replace("'", "''"),
            )
        )
        # nutrients entry
        nutrient_dict: dict[str, float] = asdict(self.nutrition)
        stmts.append(
            """\
            INSERT INTO nutrition (fdc_id, {nutrition_keys})
            VALUES ({fdc_id}, {nutrition_values});
            """.format(
                fdc_id=self.fdc_id,
                nutrition_keys=", ".join(nutrient_dict.keys()),
                nutrition_values=", ".join(map(str, nutrient_dict.values())),
            )
        )
        # portions entries
        for portion in self.portions:
            stmts.append(
                """\
                INSERT INTO portions (fdc_id, title, grams)
                VALUES ({fdc_id}, '{title}', {grams});
                """.format(
                    fdc_id=self.fdc_id,
                    title=portion.title.replace("'", "''"),
                    grams=portion.grams,
                )
            )
        return "BEGIN;" + "".join(dedent(stmt) for stmt in stmts) + "END;"
