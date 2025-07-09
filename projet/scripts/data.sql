-- Active: 1739989451833@@127.0.0.1@3306
# Client

INSERT INTO client_types (name) VALUES
('Particulier'),
('Professionnel'),
('Association');

INSERT INTO commande_status (name) VALUES
('En Attente'),
('Livrée'),
('Annulée');

INSERT INTO unite_mesures (name) VALUES
('Kilogramme'),
('Grammes'),
('Litre'),
('Millilitre'),
('Pièce');

INSERT INTO miel_types (name) VALUES
('Acacia'),
('Châtaignier'),
('Fleurs sauvages'),
('Lavande'),
('Oranger'),
('Romarin'),
('Sarrasin'),
('Tilleul');

INSERT INTO consommable_types (name, seuil_alerte, unite_id) VALUES 
('Pot de 250g', 3, 2),
('Pot de 1kg', 3, 1),
('Bouteille de 500ml', 3, 4),
('Bouteille de 1L', 3, 3);

INSERT INTO localization_status (name) VALUES
('En Service'),
('Hors Service'),
('En Réparation');

INSERT INTO mode_payements (name) VALUES
('Espèces'),
('Chèque'),
('Carte Bancaire'),
('Virement');

INSERT INTO cadre_types (name) VALUES
('Cadre Dadant'),
('Cadre Langstroth'),
('Cadre Warré');

INSERT INTO hausse_types (name, cadre_max_capacity, cadre_type_id) VALUES 
('Hausses Dadant', 10, 1),
('Hausses Langstroth', 10, 2),
('Hausses Warré', 10, 3);

INSERT INTO ruches_types (name, hausse_max_capacity, hausses_type_id) VALUES
('Ruche Dadant', 2, 1),
('Ruche Langstroth', 2, 2),
('Ruche Warré', 2, 3);

INSERT INTO ruches (description, localizations_id, ruche_type_id, created_at) VALUES
('Ruche Dadant 1', 1, 1, CURRENT_DATE),
('Ruche Langstroth 1', 1, 2, CURRENT_DATE),
('Ruche Warré 1', 1, 3, CURRENT_DATE);