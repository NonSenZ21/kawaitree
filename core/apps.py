from django.apps import AppConfig
import vinaigrette

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        # Import the model requiring translation
        from .models import Species  # or...
        from .models import Origin  # or...
        from .models import Tasklist
        from .models import Linkcat
        # Ingredient = self.get_model("Ingredient")

        # Register fields to translate
        vinaigrette.register(Species, ['name'])
        vinaigrette.register(Origin, ['name'])
        vinaigrette.register(Tasklist, ['name'])
        vinaigrette.register(Linkcat, ['name'])
