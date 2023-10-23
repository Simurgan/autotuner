from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = []
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ['user']
        return self.readonly_fields

admin.site.register(VehicleCategory)
admin.site.register(VehicleBrand)
admin.site.register(VehicleModel)
admin.site.register(VehicleYear)
admin.site.register(VehicleVersion)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    fields = ("vehicle_year", "version", "ecu_model", "potential")
    search_fields = ["vehicle_year", "version"] # cannot search on vehicle year

admin.site.register(EcuBrand)
admin.site.register(EcuModel)
admin.site.register(Ecu)
admin.site.register(ConnectionTool)

@admin.register(VehiclePotential)
class VehiclePotentialAdmin(admin.ModelAdmin): # custom page needed
    readonly_fields = []
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields
        return self.readonly_fields
    
admin.site.register(FileProcess)

@admin.register(ProcessPricing)
class ProcessPricingAdmin(admin.ModelAdmin): # custom page needed
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = []

        if obj: # editing an existing object
            return ["vehicle"]
        return self.readonly_fields

@admin.register(FileRequest)
class FileRequestAdmin(admin.ModelAdmin): # custom page needed for employee side , or readonly fields can solve the issue
    fields = ["status", "employee", "processes", "processed_file", "employee_description", "vehicle", "original_file", "customer_description", "tool", "file_type", "transmission", "tool_type"]
    readonly_fields = ["vehicle", "original_file", "customer_description", "tool", "file_type", "transmission", "tool_type", "customer"]
    list_display = ("status", "employee", "vehicle", "processes_string", "file_type", "customer")

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields
        return self.readonly_fields

admin.site.register(FileSale)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = ["customer", "type", "amount"]
    readonly_fields = ["type"]
    list_display = ("type",  "customer", "amount", "updated_at")
    
    def get_queryset(self, request):
        qs = super(TransactionAdmin, self).get_queryset(request)
        return qs.filter(type="D")

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            l = ["customer", "file_request", "file_bought", "type"]
            if obj.category != "Deposit":
                l.append("amount")
            l.extend(self.readonly_fields)
            return l
        return self.readonly_fields
    
admin.site.register(Knowledge)
admin.site.register(KnowledgePart)
admin.site.register(KnowledgeBullet)
admin.site.register(KnowledgeAd)
admin.site.register(DtcInfo)
admin.site.register(FileService) # custom page needed (only employee)
admin.site.register(FileServiceSchedule) # custom page needed (only employee)
admin.site.register(SystemSetting)
