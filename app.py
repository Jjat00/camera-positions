import os
from routes.index import *

if __name__ == '__main__':
    PORT = os.getenv("PORT", default=5001)
    app.run("0.0.0.0", debug=False, port=PORT)
