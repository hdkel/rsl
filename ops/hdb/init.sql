CREATE TABLE heroes (
    "id" serial PRIMARY KEY,
    "name" TEXT,
    "faction" TEXT,
    "rarity" TEXT,
    "role" TEXT,
    "affinity" TEXT,
    "tomes" int2,
    "bast_stats" JSONB,
    'ayumi_ranking' JSONB,
);