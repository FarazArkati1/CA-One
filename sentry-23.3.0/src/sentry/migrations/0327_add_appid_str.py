# Generated by Django 2.2.28 on 2022-10-19 13:52

from django.db import migrations, models

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

    # This flag is used to decide whether to run this migration in a transaction or not. Generally
    # we don't want to run in a transaction here, since for long running operations like data
    # back-fills this results in us locking an increasing number of rows until we finally commit.
    atomic = False

    dependencies = [
        ("sentry", "0326_add_first_transaction_to_release_project"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    """
                    ALTER TABLE "sentry_appconnectbuild" ADD COLUMN "app_id_str" varchar(256) NOT NULL DEFAULT '0';
                    """,
                    reverse_sql="""
                    ALTER TABLE "sentry_appconnectbuild" DROP COLUMN "app_id_str";
                    """,
                    hints={"tables": ["sentry_appconnectbuild"]},
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="appconnectbuild",
                    name="app_id_str",
                    field=models.CharField(default="0", max_length=256),
                ),
            ],
        )
    ]
