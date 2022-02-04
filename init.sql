PRAGMA synchronous = OFF;
PRAGMA journal_mode = OFF;

CREATE TABLE ingredients (
    fdc_id INTEGER NOT NULL PRIMARY KEY,
    fdc_date DATE,
    title TEXT
);

CREATE TABLE nutrition (
    fdc_id INTEGER NOT NULL,
    energy_kcal REAL NOT NULL,
    carbs_total_g REAL NOT NULL,
    carbs_fibre_g REAL NOT NULL,
    carbs_sugar_g REAL NOT NULL,
    fat_total_g REAL NOT NULL,
    fat_mono_g REAL NOT NULL,
    fat_poly_g REAL NOT NULL,
    fat_sat_g REAL NOT NULL,
    fat_trans_g REAL NOT NULL,
    protein_g REAL NOT NULL,
    calcium_mg REAL NOT NULL,
    folate_ug REAL NOT NULL,
    iron_mg REAL NOT NULL,
    magnesium_mg REAL NOT NULL,
    niacin_mg REAL NOT NULL,
    potassium_mg REAL NOT NULL,
    riboflavin_mg REAL NOT NULL,
    selenium_ug REAL NOT NULL,
    sodium_mg REAL NOT NULL,
    thiamin_mg REAL NOT NULL,
    vitamin_a_ug REAL NOT NULL,
    vitamin_b12_ug REAL NOT NULL,
    vitamin_b6_mg REAL NOT NULL,
    vitamin_c_mg REAL NOT NULL,
    vitamin_d_ug REAL NOT NULL,
    vitamin_e_mg REAL NOT NULL,
    zinc_mg REAL NOT NULL,
    cholestorol_mg REAL NOT NULL,
    FOREIGN KEY (fdc_id) REFERENCES ingredients(fdc_id)
);

CREATE TABLE portions (
    fdc_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    grams REAL NOT NULL,
    FOREIGN KEY (fdc_id) REFERENCES ingredients(fdc_id)
);
