"""
Compatibilidad del driver MySQL con Django.

PyMySQL es un driver de MySQL escrito en Python puro. Django espera el modulo
"MySQLdb", por lo que se registra PyMySQL como su reemplazo. Asi la conexion a
MySQL funciona sin necesidad de compilar mysqlclient en Windows.
"""

import pymysql

pymysql.install_as_MySQLdb()
