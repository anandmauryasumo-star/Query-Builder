def classFactory(iface):
    from .query_builder import QueryBuilder
    return QueryBuilder(iface)
