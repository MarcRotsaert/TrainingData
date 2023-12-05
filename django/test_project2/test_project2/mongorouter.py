
class MongoRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'test_polar':
            # xx
            return 'default'
        return "sqlite"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'test_polar':
            return 'default'
        return "sqlite"

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations only if both objects are in 'your_app_name'
        if obj1._meta.app_label == 'test_polar' and obj2._meta.app_label == 'test_polar':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Allow migrations only for models in 'your_app_name'
        if app_label == 'test_polar':
            return db == 'default'
        return db == 'sqlite'
