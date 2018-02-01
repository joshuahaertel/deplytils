"""Decorators"""


class class_property(object):  # pylint: disable=invalid-name
    """
    Decorator to make a classmethod behave like a property
    """
    def __init__(self, method):
        self.method = method
        self.name = method.__name__
        self.__doc__ = getattr(method, '__doc__')
        self.class_ = None

    def __get__(self, instance, owner):
        assert owner is not None and instance is None
        return self.method(owner)


# noinspection PyPep8Naming pylint: disable=invalid-name,unused-variable
class cached_class_property(class_property):
    """
    Decorator to transform a class method into a class field. The first
    time the field is accessed, the method is run. All subsequent
    accesses will return a cached value of the method.

    The cache can be invalidated by deleting the field. Note, however,
    that deleting the field before a value is in the cache will delete
    the method and corresponding field from the class forever.
    """

    def __init__(self, method):
        super(cached_class_property, self).__init__(method)
        self.is_cached = False
        self.cached_value = None

    def __get__(self, instance, owner=None):
        """
        If the cache is empty/invalidated, run the class method and
        store it in the cache. The cached value is returned.

        :param instance: self instance
        :param owner: type of the class
        :return: result of cached method call
        """
        if not self.is_cached:
            self.class_ = owner or instance.__class__
            self.cached_value = self.method(owner)
            self.is_cached = True

        return self.cached_value

    def __del__(self):
        """
        Invalidate the cache, if there is one. If there isn't one then
        delete the property from the class forever

        :return: None
        """
        if self.class_:
            setattr(self.class_, self.name, self.__class__(self.method))
