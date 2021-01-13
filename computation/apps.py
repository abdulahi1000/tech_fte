from django.apps import AppConfig


class ComputationConfig(AppConfig):
    name = 'computation'

    def ready(self):
        import computation.signals
