CREATE TABLE vehicle_types (
    id SERIAL PRIMARY KEY,
    vehicle_type VARCHAR(50) UNIQUE
);

INSERT INTO vehicle_types(vehicle_type) VALUES('motorcycle');
INSERT INTO vehicle_types(vehicle_type) VALUES('car');
INSERT INTO vehicle_types(vehicle_type) VALUES('truck');

CREATE TABLE vehicle_types_tariffs (
    id SERIAL PRIMARY KEY,
    type_id INTEGER REFERENCES vehicle_types(id) NOT NULL,
    price_per_hour DECIMAL(8, 2) NOT NULL
);

INSERT INTO vehicle_types_tariffs(type_id, price_per_hour) VALUES(1, 2.5);
INSERT INTO vehicle_types_tariffs(type_id, price_per_hour) VALUES(1, 5);
INSERT INTO vehicle_types_tariffs(type_id, price_per_hour) VALUES(1, 10);

CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    type_id INTEGER REFERENCES vehicle_types(id) NOT NULL,
    license_plate VARCHAR(30) UNIQUE
);

CREATE TABLE vehicle_stays (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    stay_id INTEGER REFERENCES vehicle_stays(id) NOT NULL,
    amount DECIMAL(11, 2) NOT NULL
);

CREATE TYPE bill AS
(
    stay_id INTEGER,
    tariff DECIMAL(8, 2),
    stay_duration INTEGER
);

CREATE OR REPLACE FUNCTION get_bill(plate_number VARCHAR)
RETURNS SETOF bill AS $$
DECLARE
    my_current_time TIMESTAMP := CURRENT_TIMESTAMP;
    stay_id INTEGER;
    tariff DECIMAL(8, 2);
    stay_duration INTEGER;
BEGIN
    SELECT vs.id,
           vtt.price_per_hour,
           EXTRACT(EPOCH FROM (my_current_time - vs.start_time))::INTEGER
    INTO stay_id, tariff, stay_duration
    FROM VEHICLE_STAYS vs
        JOIN vehicles v on v.id = vs.vehicle_id
        JOIN vehicle_types_tariffs vtt on v.type_id = vtt.type_id
    WHERE v.license_plate = plate_number
    AND END_TIME IS NULL;

    RETURN NEXT ROW(stay_id, tariff, stay_duration);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_stay_end_info(arg_stay_id INTEGER,
                                                arg_stay_duration INTEGER,
                                                arg_payment DECIMAL(11, 2))
RETURNS BOOLEAN AS $$
DECLARE
    result BOOLEAN;
BEGIN
    UPDATE vehicle_stays
    SET end_time = start_time + (arg_stay_duration || ' seconds')::INTERVAL
    WHERE id = arg_stay_id;

    INSERT INTO payments(stay_id, amount) VALUES(arg_stay_id, arg_payment);

    result := true;

    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION new_stay(arg_type VARCHAR, arg_plate_number VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    vehicle_id INTEGER;
    vehicle_type_id INTEGER;
    result BOOLEAN;
BEGIN
    SELECT id INTO vehicle_id FROM vehicles WHERE license_plate = arg_plate_number;

    CASE
        WHEN vehicle_id IS NULL THEN
            SELECT id INTO vehicle_type_id FROM vehicle_types WHERE vehicle_type = arg_type;

            INSERT INTO vehicles(type_id, license_plate)
            VALUES(vehicle_type_id, arg_plate_number);

            SELECT id INTO vehicle_id FROM vehicles WHERE license_plate = arg_plate_number;

            INSERT INTO vehicle_stays(vehicle_id, start_time) VALUES (vehicle_id, CURRENT_TIMESTAMP);
        ELSE
            INSERT INTO vehicle_stays(vehicle_id, start_time) VALUES (vehicle_id, CURRENT_TIMESTAMP);
    END CASE;

    result := true;

    RETURN result;
END;
$$ LANGUAGE plpgsql;

-----------------------------------
-- Drop PAYMENTS table
DROP TABLE IF EXISTS PAYMENTS;

-- Drop VEHICLE_STAYS table
DROP TABLE IF EXISTS VEHICLE_STAYS;

-- Drop VEHICLES table
DROP TABLE IF EXISTS VEHICLES;

-- Drop VEHICLE_TYPES table
DROP TABLE IF EXISTS VEHICLE_TYPES;

DROP FUNCTION IF EXISTS get_bill(plate_number VARCHAR);

DROP FUNCTION IF EXISTS insert_stay_end_info(arg_stay_id INTEGER,
                                             arg_stay_duration INTEGER,
                                             arg_payment DECIMAL(11, 2));
