BEGIN;

WITH hotel_data(name, city) AS (
    VALUES
        ('Hotel Aurora', 'Madrid'),
        ('Hotel Costa Azul', 'Barcelona'),
        ('Hotel Andino', 'Cusco')
),
upserted_hotels AS (
    INSERT INTO hotels (name, city)
    SELECT name, city
    FROM hotel_data
    ON CONFLICT (name) DO UPDATE
    SET city = EXCLUDED.city
    RETURNING id, name
)
INSERT INTO rooms (number, room_type, capacity, price, is_available, hotel_id)
SELECT v.number, v.room_type, v.capacity, v.price, v.is_available, h.id
FROM (
    VALUES
        ('Hotel Aurora', '101', 'Standard', 2, 85, TRUE),
        ('Hotel Aurora', '102', 'Standard', 2, 90, TRUE),
        ('Hotel Aurora', '103', 'Deluxe', 3, 120, TRUE),
        ('Hotel Aurora', '104', 'Deluxe', 3, 125, FALSE),
        ('Hotel Aurora', '105', 'Suite', 4, 180, TRUE),
        ('Hotel Aurora', '106', 'Family', 4, 190, TRUE),
        ('Hotel Aurora', '107', 'Standard', 2, 80, FALSE),
        ('Hotel Aurora', '108', 'Superior', 2, 140, TRUE),
        ('Hotel Aurora', '109', 'Standard', 2, 88, TRUE),
        ('Hotel Aurora', '110', 'Deluxe', 3, 130, TRUE),
        ('Hotel Aurora', '111', 'Suite', 4, 210, FALSE),
        ('Hotel Aurora', '112', 'Family', 5, 220, TRUE),
        ('Hotel Aurora', '113', 'Economy', 1, 70, TRUE),
        ('Hotel Aurora', '114', 'Deluxe', 2, 135, TRUE),
        ('Hotel Aurora', '115', 'Superior', 3, 155, FALSE),
        ('Hotel Aurora', '116', 'Suite', 4, 250, TRUE),
        ('Hotel Aurora', '117', 'Economy', 1, 60, TRUE),

        ('Hotel Costa Azul', '201', 'Standard', 2, 95, TRUE),
        ('Hotel Costa Azul', '202', 'Standard', 2, 100, FALSE),
        ('Hotel Costa Azul', '203', 'Deluxe', 3, 145, TRUE),
        ('Hotel Costa Azul', '204', 'Deluxe', 3, 150, TRUE),
        ('Hotel Costa Azul', '205', 'Suite', 4, 230, TRUE),
        ('Hotel Costa Azul', '206', 'Family', 4, 210, FALSE),
        ('Hotel Costa Azul', '207', 'Standard', 2, 92, TRUE),
        ('Hotel Costa Azul', '208', 'Superior', 2, 160, TRUE),
        ('Hotel Costa Azul', '209', 'Standard', 1, 75, TRUE),
        ('Hotel Costa Azul', '210', 'Deluxe', 3, 155, FALSE),
        ('Hotel Costa Azul', '211', 'Suite', 4, 260, TRUE),
        ('Hotel Costa Azul', '212', 'Family', 5, 240, TRUE),
        ('Hotel Costa Azul', '213', 'Economy', 1, 65, TRUE),
        ('Hotel Costa Azul', '214', 'Deluxe', 2, 140, TRUE),
        ('Hotel Costa Azul', '215', 'Superior', 3, 170, TRUE),
        ('Hotel Costa Azul', '216', 'Suite', 4, 280, FALSE),
        ('Hotel Costa Azul', '217', 'Standard', 2, 98, TRUE),

        ('Hotel Andino', '301', 'Standard', 2, 110, TRUE),
        ('Hotel Andino', '302', 'Standard', 2, 115, TRUE),
        ('Hotel Andino', '303', 'Deluxe', 3, 160, TRUE),
        ('Hotel Andino', '304', 'Deluxe', 3, 165, FALSE),
        ('Hotel Andino', '305', 'Suite', 4, 250, TRUE),
        ('Hotel Andino', '306', 'Family', 4, 225, TRUE),
        ('Hotel Andino', '307', 'Standard', 2, 105, TRUE),
        ('Hotel Andino', '308', 'Superior', 2, 175, TRUE),
        ('Hotel Andino', '309', 'Standard', 1, 85, FALSE),
        ('Hotel Andino', '310', 'Deluxe', 3, 170, TRUE),
        ('Hotel Andino', '311', 'Suite', 4, 300, TRUE),
        ('Hotel Andino', '312', 'Family', 5, 260, TRUE),
        ('Hotel Andino', '313', 'Economy', 1, 70, TRUE),
        ('Hotel Andino', '314', 'Deluxe', 2, 150, TRUE),
        ('Hotel Andino', '315', 'Superior', 3, 190, FALSE),
        ('Hotel Andino', '316', 'Suite', 4, 320, TRUE)
) AS v(hotel_name, number, room_type, capacity, price, is_available)
JOIN upserted_hotels h
  ON h.name = v.hotel_name
WHERE NOT EXISTS (
    SELECT 1
    FROM rooms r
    WHERE r.hotel_id = h.id
      AND r.number = v.number
);

COMMIT;