from django.contrib import admin

from core.models import PartyType, OrganizationCategory, PassportType, DBAccess, ContactType, Party, PartyContact, \
    Organization, OrganizationHasOrganizationCategory, Person, PersonCategory, PersonHasPersonCategory, Passport, Role, \
    PartyHasRole, Relationship, RelationshipType


class PartyAdmin(admin.ModelAdmin):
    model = Party


class PartyContactAdmin(admin.ModelAdmin):
    model = PartyContact


class ContactTypeAdmin(admin.ModelAdmin):
    model = ContactType


class PartyTypeAdmin(admin.ModelAdmin):
    model = PartyType


class RoleAdmin(admin.ModelAdmin):
    model = Role


class PartyHasRoleAdmin(admin.ModelAdmin):
    model = PartyHasRole


class RelationshipAdmin(admin.ModelAdmin):
    model = Relationship


class RelationshipTypeAdmin(admin.ModelAdmin):
    model = RelationshipType


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization


class OrganizationCategoryAdmin(admin.ModelAdmin):
    model = OrganizationCategory


class OrganizationHasOrganizationCategoryAdmin(admin.ModelAdmin):
    model = OrganizationHasOrganizationCategory


class PersonAdmin(admin.ModelAdmin):
    model = Person


class PersonCategoryAdmin(admin.ModelAdmin):
    model = PersonCategory


class PersonHasPersonCategoryAdmin(admin.ModelAdmin):
    model = PersonHasPersonCategory


class PassportAdmin(admin.ModelAdmin):
    model = Passport


class PassportTypeAdmin(admin.ModelAdmin):
    model = PassportType


class DBAccessAdmin(admin.ModelAdmin):
    model = DBAccess


admin.site.register(Party, PartyAdmin)
admin.site.register(PartyContact, PartyContactAdmin)
admin.site.register(ContactType, ContactTypeAdmin)
admin.site.register(PartyType, PartyTypeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(PartyHasRole, PartyHasRoleAdmin)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(RelationshipType, RelationshipTypeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationCategory, OrganizationCategoryAdmin)
admin.site.register(OrganizationHasOrganizationCategory, OrganizationHasOrganizationCategoryAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonCategory, PersonCategoryAdmin)
admin.site.register(PersonHasPersonCategory, PersonHasPersonCategoryAdmin)
admin.site.register(Passport, PassportAdmin)
admin.site.register(PassportType, PassportTypeAdmin)
admin.site.register(DBAccess, DBAccessAdmin)
