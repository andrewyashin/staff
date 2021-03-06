from django.contrib import admin

from core.models import PartyType, OrganizationCategory, PassportType, ContactType, Party, PartyContact, \
    Organization, OrganizationHasOrganizationCategory, Person, PersonCategory, PersonHasPersonCategory, Passport,  \
    Relationship, RelationshipType


class PartyAdmin(admin.ModelAdmin):
    model = Party


class PartyContactAdmin(admin.ModelAdmin):
    model = PartyContact


class ContactTypeAdmin(admin.ModelAdmin):
    model = ContactType


class PartyTypeAdmin(admin.ModelAdmin):
    model = PartyType


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


admin.site.register(Party, PartyAdmin)
admin.site.register(PartyContact, PartyContactAdmin)
admin.site.register(ContactType, ContactTypeAdmin)
admin.site.register(PartyType, PartyTypeAdmin)
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
