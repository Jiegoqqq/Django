START TRANSACTION;

CREATE TABLE IF NOT EXISTS `c_elegans` (
    `Wormbase_ID` TEXT,
    `Live` TEXT,
    `Gene_Sequence` TEXT,
    `Gene_Name` TEXT,
    `Other_Name` TEXT,
    PRIMARY KEY (`Wormbase_ID`(191), `Gene_Sequence`(191), `Gene_Name`(191), `Other_Name`(191))
);


COMMIT;
