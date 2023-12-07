# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Gene(models.Model):
    gene_id = models.CharField(db_column='Gene_ID', primary_key=True, max_length=14)  # Field name made lowercase.
    transcript_id = models.CharField(db_column='Transcript_ID', max_length=452, blank=True, null=True)  # Field name made lowercase.
    numbers = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Gene'


class Srr3882728HybRnaupRnaupMirandaMirandaMutation(models.Model):
    clashread = models.CharField(db_column='CLASHRead', primary_key=True, max_length=41)  # Field name made lowercase.
    readcount = models.CharField(max_length=9, blank=True, null=True)
    smallrnaname = models.CharField(db_column='SmallRNAName', max_length=16, blank=True, null=True)  # Field name made lowercase.
    regiononclashreadidentifiedassmallrna = models.CharField(db_column='RegiononCLASHReadidentifiedasSmallRNA', max_length=37, blank=True, null=True)  # Field name made lowercase.
    smallrnaregionfoundinclashread = models.CharField(db_column='SmallRNARegionFoundinCLASHRead', max_length=30, blank=True, null=True)  # Field name made lowercase.
    targetrnaname = models.CharField(db_column='TargetRNAName', max_length=14, blank=True, null=True)  # Field name made lowercase.
    regiononclashreadidentifiedastargetrna = models.CharField(db_column='RegiononCLASHReadidentifiedasTargetRNA', max_length=38, blank=True, null=True)  # Field name made lowercase.
    targetrnaregionfoundinclashread = models.CharField(db_column='TargetRNARegionFoundinCLASHRead', max_length=31, blank=True, null=True)  # Field name made lowercase.
    rnaupmaxregulatorsequence = models.CharField(db_column='RNAupMaxRegulatorsequence', max_length=36, blank=True, null=True)  # Field name made lowercase.
    rnaupmaxtargetsequence = models.CharField(db_column='RNAupMaxTargetsequence', max_length=36, blank=True, null=True)  # Field name made lowercase.
    rnaupmaxbindingsite = models.CharField(db_column='RNAupMaxbindingsite', max_length=19, blank=True, null=True)  # Field name made lowercase.
    rnaupmaxscore = models.CharField(db_column='RNAupMaxscore', max_length=13, blank=True, null=True)  # Field name made lowercase.
    rnaupregulatorsequence = models.CharField(db_column='RNAupRegulatorsequence', max_length=33, blank=True, null=True)  # Field name made lowercase.
    rnauptargetsequence = models.CharField(db_column='RNAupTargetsequence', max_length=33, blank=True, null=True)  # Field name made lowercase.
    rnaupbindingsite = models.CharField(db_column='RNAupbindingsite', max_length=16, blank=True, null=True)  # Field name made lowercase.
    rnaupscore = models.CharField(db_column='RNAupscore', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mirandaenergy = models.CharField(db_column='Mirandaenergy', max_length=13, blank=True, null=True)  # Field name made lowercase.
    mirandascore = models.CharField(db_column='Mirandascore', max_length=12, blank=True, null=True)  # Field name made lowercase.
    mirandabindingsite = models.CharField(db_column='Mirandabindingsite', max_length=18, blank=True, null=True)  # Field name made lowercase.
    mirandatargetsequence = models.CharField(db_column='MirandaTargetsequence', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mirandaregulatorsequence = models.CharField(db_column='MirandaRegulatorsequence', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mirandamaxenergy = models.CharField(db_column='MirandaMaxenergy', max_length=16, blank=True, null=True)  # Field name made lowercase.
    mirandamaxscore = models.CharField(db_column='MirandaMaxscore', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mirandamaxbindingsite = models.CharField(db_column='MirandaMaxbindingsite', max_length=21, blank=True, null=True)  # Field name made lowercase.
    mirandamaxtargetsequence = models.CharField(db_column='MirandaMaxTargetsequence', max_length=31, blank=True, null=True)  # Field name made lowercase.
    mirandamaxregulatorsequence = models.CharField(db_column='MirandaMaxRegulatorsequence', max_length=31, blank=True, null=True)  # Field name made lowercase.
    d = models.CharField(db_column='D', max_length=5, blank=True, null=True)  # Field name made lowercase.
    m = models.CharField(db_column='M', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SRR3882728_hyb_RNAup_RNAup_miranda_miranda_mutation'


class TcgaAccGenesFpkmCufflinks(models.Model):
    gene_name = models.CharField(primary_key=True, max_length=22)
    stage_1 = models.CharField(max_length=388, blank=True, null=True)
    stage_2 = models.CharField(max_length=1532, blank=True, null=True)
    stage_3 = models.CharField(max_length=649, blank=True, null=True)
    stage_4 = models.CharField(max_length=600, blank=True, null=True)
    all_stage = models.CharField(max_length=2230, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TCGA_ACC_genes_FPKM_Cufflinks'


class TcgaAccIsoformsFpkmCufflinks(models.Model):
    isoform_name = models.CharField(primary_key=True, max_length=15)
    stage_1 = models.CharField(max_length=348, blank=True, null=True)
    stage_2 = models.CharField(max_length=1404, blank=True, null=True)
    stage_3 = models.CharField(max_length=606, blank=True, null=True)
    stage_4 = models.CharField(max_length=560, blank=True, null=True)
    all_stage = models.CharField(max_length=1962, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TCGA_ACC_isoforms_FPKM_Cufflinks'


class W289All(models.Model):
    gene_id = models.CharField(db_column='Gene_ID', max_length=14, blank=True, null=True)  # Field name made lowercase.
    gene_name = models.CharField(db_column='Gene_name', max_length=13, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=24, blank=True, null=True)  # Field name made lowercase.
    transcript_id = models.CharField(db_column='Transcript_ID', primary_key=True, max_length=14)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'W289_All'


class WtCrisprWago1FlagIpSrnaSeqBedgraph(models.Model):
    init_pos = models.CharField(max_length=5, blank=True, null=True)
    end_pos = models.CharField(max_length=5, blank=True, null=True)
    evenly_rc = models.CharField(max_length=18, blank=True, null=True)
    ref_id = models.CharField(max_length=14, blank=True, null=True)
    id = models.CharField(db_column='ID', primary_key=True, max_length=6)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WT_CRISPR_WAGO_1_FLAG_IP_sRNA_seq_bedgraph'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CElegans(models.Model):
    wormbase_id = models.CharField(db_column='Wormbase_ID', primary_key=True, max_length=14)  # Field name made lowercase.
    live = models.CharField(db_column='Live', max_length=10, blank=True, null=True)  # Field name made lowercase.
    gene_sequence = models.CharField(db_column='Gene_Sequence', max_length=13, blank=True, null=True)  # Field name made lowercase.
    gene_name = models.CharField(db_column='Gene_Name', max_length=13, blank=True, null=True)  # Field name made lowercase.
    other_name = models.CharField(db_column='Other_Name', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'c_elegans'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class WtclashHybFinalWeb(models.Model):
    id = models.BigIntegerField(primary_key=True)
    clash_read = models.TextField(db_column='CLASH Read', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    region_on_clash_read_identified_as_regulator_rna = models.TextField(db_column='Region on CLASH Read identified as Regulator RNA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    region_on_clash_read_identified_as_target_rna = models.TextField(db_column='Region on CLASH Read identified as Target RNA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    read_count = models.BigIntegerField(db_column='Read Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    regulator_rna_name = models.TextField(db_column='Regulator RNA Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    regulator_rna_sequence = models.TextField(db_column='Regulator RNA Sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    regulator_rna_region_found_in_clash_read = models.TextField(db_column='Regulator RNA Region Found in CLASH Read', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    target_rna_name = models.TextField(db_column='Target RNA Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    target_rna_region_found_in_clash_read = models.TextField(db_column='Target RNA Region Found in CLASH Read', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pirscan_min_ex_binding_site = models.TextField(db_column='pirscan min_ex binding site', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pirscan_min_ex_target_sequence = models.TextField(db_column='pirscan min_ex Target sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pirscan_min_ex_score = models.FloatField(db_column='pirscan min_ex score', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pirscan_max_ex_binding_site = models.TextField(db_column='pirscan max_ex binding site', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pirscan_max_ex_target_sequence = models.TextField(db_column='pirscan max_ex Target sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pirscan_max_ex_score = models.FloatField(db_column='pirscan max_ex score', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rnaup_min_ex_regulator_rna_sequence = models.TextField(db_column='RNAup min_ex Regulator RNA sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_min_ex_target_rna_sequence = models.TextField(db_column='RNAup min_ex Target RNA sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_min_ex_binding_site = models.TextField(db_column='RNAup min_ex binding site', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_min_ex_score = models.FloatField(db_column='RNAup min_ex score', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_regulator_rna_sequence = models.TextField(db_column='RNAup max_ex Regulator RNA sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_target_rna_sequence = models.TextField(db_column='RNAup max_ex Target RNA sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_binding_site = models.TextField(db_column='RNAup max_ex binding site', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_score = models.FloatField(db_column='RNAup max_ex score', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d = models.TextField(db_column='D', blank=True, null=True)  # Field name made lowercase.
    m = models.TextField(db_column='M', blank=True, null=True)  # Field name made lowercase.
    wt_wago_pirscan_min_ex25_22g = models.FloatField(db_column='WT_WAGO_pirscan min_ex25_22G', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wt_wago_pirscan_max_ex25_22g = models.FloatField(db_column='WT_WAGO_pirscan max_ex25_22G', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wt_wago_rnaup_min_ex25_22g = models.FloatField(db_column='WT_WAGO_RNAup min_ex25_22G', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wt_wago_rnaup_max_ex25_22g = models.FloatField(db_column='WT_WAGO_RNAup max_ex25_22G', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mutation_count = models.BigIntegerField(blank=True, null=True)
    mutation_pos = models.TextField(blank=True, null=True)
    algorithm = models.TextField(blank=True, null=True)
    pirscan_min_ex_22g_pvalue_corrected = models.FloatField(db_column='pirscan min_ex 22G pvalue-corrected', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pirscan_max_ex_22g_pvalue_corrected = models.FloatField(db_column='pirscan max_ex 22G pvalue-corrected', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_min_ex_22g_pvalue_corrected = models.FloatField(db_column='RNAup min_ex 22G pvalue-corrected', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_22g_pvalue_corrected = models.FloatField(db_column='RNAup max_ex 22G pvalue-corrected', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mutation_string = models.TextField(blank=True, null=True)
    prg1mut_wago1_22g_rnaup_min_ex25 = models.FloatField(db_column='PRG1MUT_WAGO1_22G_RNAup min_ex25', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prg1mut_wago1_22g_pirscan_min_ex25 = models.FloatField(db_column='PRG1MUT_WAGO1_22G_pirscan min_ex25', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prg1mut_wago1_22g_rnaup_max_ex25 = models.FloatField(db_column='PRG1MUT_WAGO1_22G_RNAup max_ex25', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prg1mut_wago1_22g_pirscan_max_ex25 = models.FloatField(db_column='PRG1MUT_WAGO1_22G_pirscan max_ex25', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wago1_22g_rnaup_min_ex25_foldchange = models.FloatField(db_column='WAGO1_22G_RNAup min_ex25 foldchange', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wago1_22g_pirscan_max_ex25_foldchange = models.FloatField(db_column='WAGO1_22G_pirscan max_ex25 foldchange', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wago1_22g_rnaup_max_ex25_foldchange = models.FloatField(db_column='WAGO1_22G_RNAup max_ex25 foldchange', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wago1_22g_pirscan_min_ex25_foldchange = models.FloatField(db_column='WAGO1_22G_pirscan min_ex25 foldchange', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'wtCLASH_hyb_final_web'
