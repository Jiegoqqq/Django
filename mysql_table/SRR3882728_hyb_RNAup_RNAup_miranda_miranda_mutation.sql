START TRANSACTION;

CREATE TABLE IF NOT EXISTS `SRR3882728_hyb_RNAup_RNAup_miranda_miranda_mutation` (
    `CLASHRead` TEXT,
    `readcount` INTEGER,
    `SmallRNAName` TEXT,
    `RegiononCLASHReadidentifiedasSmallRNA` TEXT,
    `SmallRNARegionFoundinCLASHRead` TEXT,
    `TargetRNAName` TEXT,
    `RegiononCLASHReadidentifiedasTargetRNA` TEXT,
    `TargetRNARegionFoundinCLASHRead` TEXT,
    `RNAupMaxRegulatorsequence` TEXT,
    `RNAupMaxTargetsequence` TEXT,
    `RNAupMaxbindingsite` TEXT,
    `RNAupMaxscore` FLOAT,
    `RNAupRegulatorsequence` TEXT,
    `RNAupTargetsequence` TEXT,
    `RNAupbindingsite` TEXT,
    `RNAupscore` FLOAT,
    `Mirandaenergy` FLOAT,
    `Mirandascore` FLOAT,
    `Mirandabindingsite` TEXT,
    `MirandaTargetsequence` TEXT,
    `MirandaRegulatorsequence` TEXT,
    `MirandaMaxenergy` FLOAT,
    `MirandaMaxscore` FLOAT,
    -- Other columns
    PRIMARY KEY (`CLASHRead`(255)) 
);

COMMIT;
