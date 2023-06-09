# Generated by Django 2.2.28 on 2023-02-28 23:54

from django.db import migrations

import sentry.db.models.fields.hybrid_cloud_foreign_key
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
        ("sentry", "0368_monitor_remove_slug_nullable"),
    ]

    database_operations = [
        migrations.AlterField(
            model_name="useroption",
            name="organization",
            field=sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                to="sentry.Organization", db_constraint=False, db_index=True, null=True
            ),
        ),
        migrations.AlterField(
            model_name="useroption",
            name="project",
            field=sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                to="sentry.Project", db_constraint=False, db_index=True, null=True
            ),
        ),
    ]

    state_operations = [
        migrations.AlterField(
            model_name="useroption",
            name="organization",
            field=sentry.db.models.fields.hybrid_cloud_foreign_key.HybridCloudForeignKey(
                "sentry.Organization", null=True, on_delete="CASCADE"
            ),
        ),
        migrations.RenameField(
            model_name="useroption",
            old_name="organization",
            new_name="organization_id",
        ),
        migrations.AlterField(
            model_name="useroption",
            name="project",
            field=sentry.db.models.fields.hybrid_cloud_foreign_key.HybridCloudForeignKey(
                "sentry.Project", null=True, on_delete="CASCADE"
            ),
        ),
        migrations.RenameField(
            model_name="useroption",
            old_name="project",
            new_name="project_id",
        ),
        migrations.AlterUniqueTogether(
            name="useroption",
            unique_together=(("user", "project_id", "key"), ("user", "organization_id", "key")),
        ),
    ]

    operations = database_operations + [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
