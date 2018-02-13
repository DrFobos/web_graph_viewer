ALLOWED_EXTENSIONS = {'xlsx', 'xls'}


# Check if file extension fulfill the requirements
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
