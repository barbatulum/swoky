# Done

def make_kwargs(compatibles=None, **kwargs):
    if compatibles is None:
        compatibles = []
    output_kwargs = {}
    for key in kwargs:
        if key == 'compatible_kwargs':
            continue
        output_kwargs[key] = kwargs[key]
    return output_kwargs