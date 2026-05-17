def register(library):
    from .platform import IonQPlatform
    library.register(IonQPlatform)
