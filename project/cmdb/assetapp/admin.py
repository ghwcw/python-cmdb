from assetapp import assetapp_handler_view
from assetapp import models
from django.contrib import admin


# Register your models here.

class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
    list_filter = ['asset_type', 'manufacturer', 'c_time']
    search_fields = ['sn']

    # admin中的动作actions，和上面一样也是固定属性
    actions = ['approve_selected_new_assets']

    # 获得被打钩的checkbox对应的资产,然后进行审批动作
    def approve_selected_new_assets(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        success_upline_number = 0
        for asset_id in selected:
            appro = assetapp_handler_view.ApproveAsset(request, asset_id)
            ret = appro.asset_upline()
            if ret:
                success_upline_number += 1
        # 顶部绿色提示信息
        self.message_user(request, message='成功批准 %s 条新资产上线！' % success_upline_number)

    # 为action提供中文描述
    approve_selected_new_assets.short_description = "批准选择的新资产"


class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'name', 'status', 'approved_by', 'c_time', "m_time"]


# ------------------------
admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.StorageDevice)
admin.site.register(models.SecurityDevice)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Contract)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.EventLog)
admin.site.register(models.IDC)
admin.site.register(models.Manufacturer)
admin.site.register(models.NetworkDevice)
admin.site.register(models.NIC)
admin.site.register(models.RAM)
admin.site.register(models.Software)
admin.site.register(models.Tag)
admin.site.register(models.NewAssetApprovalZone, NewAssetApprovalZoneAdmin)
