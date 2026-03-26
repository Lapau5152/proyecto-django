import pymysql
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

# 1. Driver y Versión del conector
pymysql.install_as_MySQLdb()
pymysql.version_info = (2, 2, 1, "final", 0)

# 2. Truco para saltar el chequeo de MariaDB 10.6
def dummy_check_database_version_supported(self):
    return
BaseDatabaseWrapper.check_database_version_supported = dummy_check_database_version_supported

# 3. EL TRUCO PARA EL ERROR 'RETURNING':
# Esto le dice a Django: "Mi base de datos NO soporta RETURNING"
DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)