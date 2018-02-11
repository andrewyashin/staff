from core.submodels.organization_models import *
from core.submodels.party_models import *
from core.submodels.person_models import *


class DBAccess(models.Model):
    login = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    startDate = models.DateField
    endDate = models.DateField
