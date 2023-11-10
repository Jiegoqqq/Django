START TRANSACTION;

CREATE TABLE IF NOT EXISTS `W289_All` (
    `Gene_ID` VARCHAR(255), -- Use an appropriate length
    `Gene_name` TEXT,
    `Type` TEXT,
    `Transcript_ID` TEXT,
    PRIMARY KEY (`Gene_ID`(255), `Type`(255), `Transcript_ID`(255))
);

COMMIT;
