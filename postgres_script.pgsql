CREATE TABLE VEHICLE_TYPES (
    Id SERIAL PRIMARY KEY,
    VehicleType VARCHAR(50) UNIQUE
);

CREATE TABLE VEHICLES (
    Id SERIAL PRIMARY KEY,
    TypeId INTEGER REFERENCES VEHICLE_TYPES(Id),
    LicensePlate VARCHAR(30) UNIQUE
);

CREATE TABLE VEHICLE_STAYS (
    Id SERIAL PRIMARY KEY,
    VehicleId INTEGER REFERENCES VEHICLES(Id),
    StartTime TIMESTAMP NOT NULL,
    EndTime TIMESTAMP NULL
);

CREATE TABLE PAYMENTS (
    Id SERIAL PRIMARY KEY,
    StayId INTEGER REFERENCES VEHICLE_STAYS(Id),
    Amount DECIMAL(12, 2) NOT NULL
);


CREATE OR REPLACE FUNCTION update_stay_duration(plate_number VARCHAR)
RETURNS INTEGER AS $$
DECLARE
    stay_duration INTEGER;
BEGIN
    -- Find the stay with the provided license plate and no end_time
    SELECT EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - START_TIME))::INTEGER INTO stay_duration
    FROM VEHICLE_STAYS
    WHERE VEHICLE_ID = (
        SELECT ID
        FROM VEHICLES
        WHERE LICENSE_PLATE = plate_number
    )
    AND END_TIME IS NULL;

    -- Update the end_time with the current time
    UPDATE VEHICLE_STAYS
    SET END_TIME = CURRENT_TIMESTAMP
    WHERE VEHICLE_ID = (
        SELECT ID
        FROM VEHICLES
        WHERE LICENSE_PLATE = plate_number
    )
    AND END_TIME IS NULL;

    -- Return the stay duration in seconds
    RETURN stay_duration;
END;
$$ LANGUAGE plpgsql;

