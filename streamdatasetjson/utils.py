import ijson


def reread_prefix(f, prefix):
    """
    Reads the file form the start and retrieves the values for the given prefix.
    """
    f.seek(0)
    return ijson.items(f, prefix)


def load_prefix(f, prefix):
    """
    Re-reads the file looking for the given prefix, and loads the result into memory.
    """
    return next(reread_prefix(f, prefix))
