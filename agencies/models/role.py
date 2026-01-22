from utils.base_model import BaseModel

class Role(BaseModel):
    """
    Represents a role that can be assigned to employees at an agency.
    Example roles: 'Manager', 'Agent', 'Admin', 'Support'
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='agency_roles'
    )
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name