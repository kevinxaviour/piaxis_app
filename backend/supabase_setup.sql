-- TABLES
CREATE TABLE details (
    id SERIAL PRIMARY KEY,
    title TEXT,
    category TEXT,
    tags TEXT,
    description TEXT,
    source TEXT DEFAULT 'standard',
    user_id INT
);

CREATE TABLE detail_usage_rules (
    id SERIAL PRIMARY KEY,
    detail_id INT REFERENCES details(id),
    host_element TEXT,
    adjacent_element TEXT,
    exposure TEXT
);

-- LOAD DATA
INSERT INTO details (id,title,category,tags,description,source)
VALUES
(1,'External Wall – Slab Junction','Waterproofing',
'wall,slab,waterproofing,external',
'Waterproof membrane continuity at external wall and slab junction','standard'),

(2,'Window Sill Detail with Drip','Window',
'window,sill,drip,external',
'External window sill detail with drip groove','standard'),

(3,'Internal Wall – Floor Junction','Wall',
'wall,floor,internal',
'Junction detail between internal wall and finished floor','user_project');

INSERT INTO detail_usage_rules (id,detail_id,host_element,adjacent_element,exposure)
VALUES
(1,1,'External Wall','Slab','External'),
(2,2,'Window','External Wall','External'),
(3,3,'Internal Wall','Floor','Internal');