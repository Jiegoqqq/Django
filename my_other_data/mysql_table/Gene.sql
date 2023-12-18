START TRANSACTION;

CREATE TABLE IF NOT EXISTS `Gene` (
    `Gene_ID` VARCHAR(255), -- Use an appropriate length
    `Transcript_ID` TEXT,
    `numbers` INTEGER,
    PRIMARY KEY (`Gene_ID`(255))
);
COMMIT;
