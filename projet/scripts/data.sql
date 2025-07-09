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