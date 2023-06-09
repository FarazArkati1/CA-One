# Generated by Django 2.2.28 on 2023-02-27 10:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import sentry.db.models.fields.bounded
import sentry.db.models.fields.foreignkey
from sentry.new_migrations.migrations import CheckedMigration


class Migration(CheckedMigration):
    # This flag is used to mark that a migration shouldn't be automatically run in production. For
    # the most part, this should only be used for operations where it's safe to run the migration
    # after your code has deployed. So this should not be used for most operations that alter the
    # schema of a table.
    # Here are some things that make sense to mark as dangerous:
    # - Large data migrations. Typically we want these to be run manually by ops so that they can
    #   be monitored and not block the deploy for a long period of time while they run.
    # - Adding indexes to large tables. Since this can take a long time, we'd generally prefer to
    #   have ops run this and not block the deploy. Note that while adding an index is a schema
    #   change, it's completely safe to run the operation after the code has deployed.
    is_dangerous = False

    dependencies = [
        ("sentry", "0362_break_project_integration_fk"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtifactBundle",
            fields=[
                (
                    "id",
                    sentry.db.models.fields.bounded.BoundedBigAutoField(
                        primary_key=True, serialize=False
                    ),
                ),
                (
                    "organization_id",
                    sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
                ),
                ("bundle_id", models.UUIDField(null=True)),
                ("artifact_count", sentry.db.models.fields.bounded.BoundedPositiveIntegerField()),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "file",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sentry.File"
                    ),
                ),
            ],
            options={
                "db_table": "sentry_artifactbundle",
                "unique_together": {("organization_id", "bundle_id")},
            },
        ),
        migrations.CreateModel(
            name="ReleaseArtifactBundle",
            fields=[
                (
                    "id",
                    sentry.db.models.fields.bounded.BoundedBigAutoField(
                        primary_key=True, serialize=False
                    ),
                ),
                (
                    "organization_id",
                    sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
                ),
                ("release_name", models.CharField(max_length=250)),
                ("dist_id", sentry.db.models.fields.bounded.BoundedBigIntegerField(null=True)),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "artifact_bundle",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sentry.ArtifactBundle"
                    ),
                ),
            ],
            options={
                "db_table": "sentry_releaseartifactbundle",
                "unique_together": {
                    ("organization_id", "release_name", "dist_id", "artifact_bundle")
                },
            },
        ),
        migrations.CreateModel(
            name="ProjectArtifactBundle",
            fields=[
                (
                    "id",
                    sentry.db.models.fields.bounded.BoundedBigAutoField(
                        primary_key=True, serialize=False
                    ),
                ),
                (
                    "organization_id",
                    sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
                ),
                (
                    "project_id",
                    sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
                ),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "artifact_bundle",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sentry.ArtifactBundle"
                    ),
                ),
            ],
            options={
                "db_table": "sentry_projectartifactbundle",
                "unique_together": {("project_id", "artifact_bundle")},
            },
        ),
        migrations.CreateModel(
            name="DebugIdArtifactBundle",
            fields=[
                (
                    "id",
                    sentry.db.models.fields.bounded.BoundedBigAutoField(
                        primary_key=True, serialize=False
                    ),
                ),
                (
                    "organization_id",
                    sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
                ),
                ("debug_id", models.UUIDField()),
                ("source_file_type", models.IntegerField()),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                ("date_last_accessed", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "artifact_bundle",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sentry.ArtifactBundle"
                    ),
                ),
            ],
            options={
                "db_table": "sentry_debugidartifactbundle",
                "unique_together": {("debug_id", "artifact_bundle", "source_file_type")},
            },
        ),
    ]
