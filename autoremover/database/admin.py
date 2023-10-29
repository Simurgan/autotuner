from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from admin_auto_filters.filters import AutocompleteFilter

# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ["company_name", "phone_zone", "phone_number", "pricing_class"]
    readonly_fields = ["company_name", "phone_zone", "phone_number"]

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = []
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ['user']
        return self.readonly_fields

admin.site.register(VehicleCategory)
admin.site.register(VehicleBrand)

class VehicleYearInline(admin.TabularInline):
    model = VehicleYear
    extra = 1

@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    inlines = [VehicleYearInline]
    search_fields = ("brand__name", "name", )
    list_per_page = 20

@admin.register(VehicleYear)
class VehicleYearAdmin(admin.ModelAdmin):
    autocomplete_fields = ("model", )
    search_fields = ("model__name", "model__brand__name")
    list_per_page = 10

@admin.register(VehicleVersion)
class VehicleVersionAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_per_page = 10

class EcuModelFilter(AutocompleteFilter):
    title = 'Ecu Model'
    field_name = 'ecu_model'

class VehicleYearFilter(AutocompleteFilter):
    title = 'Vehicle Year'
    field_name = 'vehicle_year'

class PotentialInline(admin.TabularInline):
    model = VehiclePotential
    extra = 1

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    inlines = [PotentialInline]
    fields = ("vehicle_year", "version", "ecu_model")
    autocomplete_fields = ("vehicle_year", "version", "ecu_model")
    actions = ['make_pricing']
    list_filter = [EcuModelFilter, VehicleYearFilter]
    list_display = ("vehicle_year", "version", "ecu_model")
    list_per_page = 10
    
    @admin.action
    def make_pricing(self, request, queryset):
        if 'apply' in request.POST:
            vehicle_ids = request.POST.getlist("_selected_action")
            master_price = float(request.POST.get("master_price"))
            slave_price = float(request.POST.get("slave_price"))
            euro_price = float(request.POST.get("euro_price"))
            process_id = int(request.POST.get("process"))

            for vehicle_id in vehicle_ids:
                pricing, created = ProcessPricing.objects.get_or_create(vehicle_id=int(vehicle_id), process_id=process_id, defaults={
                    "master_price": master_price,
                    "slave_price": slave_price,
                    "euro_price": euro_price
                    })

                if not created:
                    pricing.master_price = master_price
                    pricing.slave_price = slave_price
                    pricing.euro_price = euro_price
                    pricing.save()
            
            self.message_user(request, "Pricing is done as " + str(master_price) + ", " + str(slave_price) + ", " + str(euro_price) + " with process id: " + str(process_id) + " on " + str(len(vehicle_ids)) + " vehicles!")
            return HttpResponseRedirect(request.get_full_path())

        processes = FileProcess.objects.all()
        context = {
            'vehicles': queryset,
            'processes': processes
        }
        return render(request, 'admin/make_pricing.html', context)

admin.site.register(EcuBrand)
@admin.register(EcuModel)
class EcuModelAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_filter = ("brand", )
    list_display = ("name", "brand")
    list_per_page = 20

admin.site.register(Ecu)
admin.site.register(ConnectionTool)
    
admin.site.register(FileProcess)

@admin.register(FileRequest)
class FileRequestAdmin(admin.ModelAdmin): # custom page needed for employee side , or readonly fields can solve the issue
    fields = ["status", "employee", "processes", "processed_file", "employee_description", "vehicle", "original_file", "customer_description", "tool", "file_type", "transmission", "tool_type", "customer"]
    readonly_fields = ["vehicle", "original_file", "customer_description", "tool", "file_type", "transmission", "tool_type", "customer"]
    list_display = ("status", "employee", "vehicle", "processes_string", "file_type", "customer")
    list_filter = ("status",)

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

@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions
