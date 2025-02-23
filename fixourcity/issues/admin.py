from django.contrib import admin
from .models import Issue, ContractorAssignment

# Register the Issue model
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'contractor', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'contractor', 'created_at')

# Register the ContractorAssignment model
@admin.register(ContractorAssignment)
class ContractorAssignmentAdmin(admin.ModelAdmin):
    list_display = ('contractor', 'issue', 'assigned_at')
    search_fields = ('contractor__name', 'issue__title')
    list_filter = ('contractor', 'assigned_at')
