# -*- coding: utf-8 -*-
from app import app

__version = 0.5
 
if  __name__ == '__main__':
    #app.debug=True
    app.run(debug=True,host="192.168.31.57",port=8080)