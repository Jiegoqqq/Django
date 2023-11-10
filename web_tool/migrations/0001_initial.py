# Generated by Django 4.2.2 on 2023-10-26 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CElegans',
            fields=[
                ('wormbase_id', models.CharField(db_column='Wormbase_ID', max_length=14, primary_key=True, serialize=False)),
                ('live', models.CharField(blank=True, db_column='Live', max_length=10, null=True)),
                ('gene_sequence', models.CharField(blank=True, db_column='Gene_Sequence', max_length=13, null=True)),
                ('gene_name', models.CharField(blank=True, db_column='Gene_Name', max_length=13, null=True)),
                ('other_name', models.CharField(blank=True, db_column='Other_Name', max_length=20, null=True)),
            ],
            options={
                'db_table': 'c_elegans',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('gene_id', models.CharField(db_column='Gene_ID', max_length=14, primary_key=True, serialize=False)),
                ('transcript_id', models.CharField(blank=True, db_column='Transcript_ID', max_length=452, null=True)),
                ('numbers', models.CharField(blank=True, max_length=7, null=True)),
            ],
            options={
                'db_table': 'Gene',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Srr3882728HybRnaupRnaupMirandaMirandaMutation',
            fields=[
                ('clashread', models.CharField(db_column='CLASHRead', max_length=41, primary_key=True, serialize=False)),
                ('readcount', models.CharField(blank=True, max_length=9, null=True)),
                ('smallrnaname', models.CharField(blank=True, db_column='SmallRNAName', max_length=16, null=True)),
                ('regiononclashreadidentifiedassmallrna', models.CharField(blank=True, db_column='RegiononCLASHReadidentifiedasSmallRNA', max_length=37, null=True)),
                ('smallrnaregionfoundinclashread', models.CharField(blank=True, db_column='SmallRNARegionFoundinCLASHRead', max_length=30, null=True)),
                ('targetrnaname', models.CharField(blank=True, db_column='TargetRNAName', max_length=14, null=True)),
                ('regiononclashreadidentifiedastargetrna', models.CharField(blank=True, db_column='RegiononCLASHReadidentifiedasTargetRNA', max_length=38, null=True)),
                ('targetrnaregionfoundinclashread', models.CharField(blank=True, db_column='TargetRNARegionFoundinCLASHRead', max_length=31, null=True)),
                ('rnaupmaxregulatorsequence', models.CharField(blank=True, db_column='RNAupMaxRegulatorsequence', max_length=36, null=True)),
                ('rnaupmaxtargetsequence', models.CharField(blank=True, db_column='RNAupMaxTargetsequence', max_length=36, null=True)),
                ('rnaupmaxbindingsite', models.CharField(blank=True, db_column='RNAupMaxbindingsite', max_length=19, null=True)),
                ('rnaupmaxscore', models.CharField(blank=True, db_column='RNAupMaxscore', max_length=13, null=True)),
                ('rnaupregulatorsequence', models.CharField(blank=True, db_column='RNAupRegulatorsequence', max_length=33, null=True)),
                ('rnauptargetsequence', models.CharField(blank=True, db_column='RNAupTargetsequence', max_length=33, null=True)),
                ('rnaupbindingsite', models.CharField(blank=True, db_column='RNAupbindingsite', max_length=16, null=True)),
                ('rnaupscore', models.CharField(blank=True, db_column='RNAupscore', max_length=10, null=True)),
                ('mirandaenergy', models.CharField(blank=True, db_column='Mirandaenergy', max_length=13, null=True)),
                ('mirandascore', models.CharField(blank=True, db_column='Mirandascore', max_length=12, null=True)),
                ('mirandabindingsite', models.CharField(blank=True, db_column='Mirandabindingsite', max_length=18, null=True)),
                ('mirandatargetsequence', models.CharField(blank=True, db_column='MirandaTargetsequence', max_length=30, null=True)),
                ('mirandaregulatorsequence', models.CharField(blank=True, db_column='MirandaRegulatorsequence', max_length=30, null=True)),
                ('mirandamaxenergy', models.CharField(blank=True, db_column='MirandaMaxenergy', max_length=16, null=True)),
                ('mirandamaxscore', models.CharField(blank=True, db_column='MirandaMaxscore', max_length=15, null=True)),
                ('mirandamaxbindingsite', models.CharField(blank=True, db_column='MirandaMaxbindingsite', max_length=21, null=True)),
                ('mirandamaxtargetsequence', models.CharField(blank=True, db_column='MirandaMaxTargetsequence', max_length=31, null=True)),
                ('mirandamaxregulatorsequence', models.CharField(blank=True, db_column='MirandaMaxRegulatorsequence', max_length=31, null=True)),
                ('d', models.CharField(blank=True, db_column='D', max_length=5, null=True)),
                ('m', models.CharField(blank=True, db_column='M', max_length=6, null=True)),
            ],
            options={
                'db_table': 'SRR3882728_hyb_RNAup_RNAup_miranda_miranda_mutation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='W289All',
            fields=[
                ('gene_id', models.CharField(blank=True, db_column='Gene_ID', max_length=14, null=True)),
                ('gene_name', models.CharField(blank=True, db_column='Gene_name', max_length=13, null=True)),
                ('type', models.CharField(blank=True, db_column='Type', max_length=24, null=True)),
                ('transcript_id', models.CharField(db_column='Transcript_ID', max_length=14, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'W289_All',
                'managed': False,
            },
        ),
    ]
