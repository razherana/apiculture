CREATE TABLE localizations (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    created_at TIMESTAMP
);

CREATE TABLE localization_status (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE localization_status_histories (
    id SERIAL PRIMARY KEY,
    localization_id INT REFERENCES localizations(id),
    localization_status_id INT REFERENCES localization_status(id),
    created_at TIMESTAMP
);

CREATE TABLE essaim_origins (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE essaim_races (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE essaim_status (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE essaims (
    id SERIAL PRIMARY KEY,
    essaim_origin_id INT REFERENCES essaim_origins(id),
    essaim_race_id INT REFERENCES essaim_races(id),
    created_at TIMESTAMP
);

CREATE TABLE essaim_status_histories (
    id SERIAL PRIMARY KEY,
    essaim_id INT REFERENCES essaims(id),
    essaim_status_id INT REFERENCES essaim_status(id),
    created_at TIMESTAMP
);

CREATE TABLE essaim_details (
    id SERIAL PRIMARY KEY,
    note TEXT,
    is_death BOOLEAN,
    essaim_id INT REFERENCES essaims(id),
    ouvrier_added INT,
    faux_bourdon_added INT,
    reine_added INT,
    created_at TIMESTAMP
);

CREATE TABLE ruche_types (
    id SERIAL PRIMARY KEY,
    name TEXT,
    hausse_max_capacity INT,
    hausse_type_id INT
);

CREATE TABLE ruche_status (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE ruche_status_histories (
    id SERIAL PRIMARY KEY,
    ruche_id INT,
    ruche_status_id INT REFERENCES ruche_status(id),
    created_at TIMESTAMP
);

CREATE TABLE ruche_hausse_histories (
    id SERIAL PRIMARY KEY,
    ruche_id INT,
    hausse_id INT,
    created_at TIMESTAMP
);

CREATE TABLE hausse_types (
    id SERIAL PRIMARY KEY,
    name TEXT,
    cadre_max_capacity INT,
    cadre_type_id INT
);

CREATE TABLE cadre_types (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE hausses (
    id SERIAL PRIMARY KEY,
    hausse_type_id INT REFERENCES hausse_types(id),
    created_at TIMESTAMP
);

CREATE TABLE hausse_cadres (
    id SERIAL PRIMARY KEY,
    hausse_id INT REFERENCES hausses(id),
    added_cadre INT,
    created_at TIMESTAMP
);

CREATE TABLE ruches (
    id SERIAL PRIMARY KEY,
    description TEXT,
    localizations_id INT REFERENCES localizations(id),
    ruche_type_id INT REFERENCES ruche_types(id),
    essaim_id INT REFERENCES essaims(id),
    created_at TIMESTAMP
);

CREATE TABLE comportements (
    id SERIAL PRIMARY KEY,
    description TEXT
);

CREATE TABLE essaim_sante_histories (
    id SERIAL PRIMARY KEY,
    essaim_id INT REFERENCES essaims(id),
    force_colonie INT,
    comportement_id INT REFERENCES comportements(id),
    egg_present BOOLEAN,
    couvain_present BOOLEAN,
    reine_present BOOLEAN,
    parasite TEXT,
    maladie TEXT,
    note TEXT,
    created_at TIMESTAMP
);

CREATE TABLE recoltes (
    id SERIAL PRIMARY KEY,
    ruche_id INT REFERENCES ruches(id),
    poids_miel FLOAT,
    taux_humidite FLOAT,
    qualite INT,
    created_at TIMESTAMP
);

CREATE TABLE materiel_types (
    id SERIAL PRIMARY KEY,
    name TEXT,
    designation TEXT,
    seuil_alerte INT
);

CREATE TABLE materiel_status (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE materiels (
    id SERIAL PRIMARY KEY,
    duree_de_vie_estimee INT,
    materiel_type_id INT REFERENCES materiel_types(id),
    created_at TIMESTAMP
);

CREATE TABLE materiel_status_histories (
    id SERIAL PRIMARY KEY,
    materiel_id INT REFERENCES materiels(id),
    materiel_status_id INT REFERENCES materiel_status(id),
    created_at TIMESTAMP
);

CREATE TABLE unite_mesures (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE consommable_types (
    id SERIAL PRIMARY KEY,
    name TEXT,
    unite_id INT REFERENCES unite_mesures(id),
    seuil_alerte INT
);

CREATE TABLE consommables (
    id SERIAL PRIMARY KEY,
    consommable_type_id INT REFERENCES consommable_types(id),
    date_de_peremption DATE,
    created_at TIMESTAMP
);

CREATE TABLE consommable_consomme (
    id SERIAL PRIMARY KEY,
    consommable_id INT REFERENCES consommables(id),
    created_at TIMESTAMP
);

CREATE TABLE miel_types (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE miels (
    id SERIAL PRIMARY KEY,
    consommable_type_id INT,
    unite_mesure_id INT REFERENCES unite_mesures(id),
    quantite_unite FLOAT,
    miel_type_id INT REFERENCES miel_types(id)
);

CREATE TABLE miel_price_histories (
    id SERIAL PRIMARY KEY,
    miel_id INT REFERENCES miels(id),
    price FLOAT,
    created_at TIMESTAMP
);

CREATE TABLE miel_stock (
    id SERIAL PRIMARY KEY,
    miel_id INT REFERENCES miels(id),
    added_quantity FLOAT,
    created_at TIMESTAMP
);

CREATE TABLE client_types (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name TEXT,
    contact TEXT,
    email TEXT,
    note TEXT,
    adresse TEXT,
    client_type_id INT REFERENCES client_types(id)
);

CREATE TABLE mode_payements (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE ventes (
    id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(id),
    mode_payement_id INT REFERENCES mode_payements(id),
    note TEXT,
    created_at TIMESTAMP
);

CREATE TABLE vente_details (
    id SERIAL PRIMARY KEY,
    miel_id INT REFERENCES miels(id),
    vente_id INT REFERENCES ventes(id),
    quantite FLOAT
);

CREATE TABLE commandes (
    id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(id),
    vente_id INT REFERENCES ventes(id),
    note TEXT,
    livraison_date DATE,
    created_at TIMESTAMP
);

CREATE TABLE commande_details (
    id SERIAL PRIMARY KEY,
    miel_id INT REFERENCES miels(id),
    commande_id INT REFERENCES commandes(id),
    quantite FLOAT
);

CREATE TABLE commande_status (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE commande_status_histories (
    id SERIAL PRIMARY KEY,
    commande_id INT REFERENCES commandes(id),
    commande_status_id INT REFERENCES commande_status(id)
);

CREATE TABLE task_types (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE task_priorites (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE task_status_type (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT,
    ruche_id INT REFERENCES ruches(id),
    localization_id INT REFERENCES localizations(id),
    task_type_id INT REFERENCES task_types(id),
    description TEXT,
    task_priorite_id INT REFERENCES task_priorites(id),
    date_prevue DATE,
    date_realisation DATE
);

CREATE TABLE task_status_histories (
    id SERIAL PRIMARY KEY,
    task_id INT REFERENCES tasks(id),
    task_status_type_id INT REFERENCES task_status_type(id),
    created_at TIMESTAMP
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    is_admin BOOLEAN,
    email TEXT UNIQUE,
    password TEXT
);

CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    role_id INT REFERENCES roles(id),
    user_id INT REFERENCES users(id)
);

CREATE TABLE login_histories (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    created_at TIMESTAMP
);

CREATE TABLE intervention_type (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE intervention (
    id SERIAL PRIMARY KEY,
    title TEXT,
    donnees TEXT,
    ruche_id INT REFERENCES ruches(id),
    localization_id INT REFERENCES localizations(id),
    intervention_type_id INT REFERENCES intervention_type(id),
    details TEXT,
    date_prevue DATE,
    date_realisation DATE
);
