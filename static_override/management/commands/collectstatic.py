from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as DjangoCollectstaticCommand,
)


class Command(DjangoCollectstaticCommand):
    pass