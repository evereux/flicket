
# used for debugging purposes only
def print_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print("Error in the {} field - {}".format(
                getattr(form, field).label.text,
                error
            ))