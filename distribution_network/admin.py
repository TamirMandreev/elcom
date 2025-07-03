from django.contrib import admin

from distribution_network.models import DistributionNetwork, NetworkParticipant, Product


# Зарегистрировать модель DistributionNetwork в панели администратора
@admin.register(DistributionNetwork)
class DistributionNetworkAdmin(admin.ModelAdmin):
    # Отобразить в списке сетей дистрибуции следующие поля
    list_display = ('factory', 'retail_network', 'individual_entrepreneur')


# Зарегистрировать модель NetworkParticipant в панели администратора
@admin.register(NetworkParticipant)
class NetworkParticipantAdmin(admin.ModelAdmin):
    # Отобразить в списке участников сети дистрибуции следующие поля
    list_display = ('type', 'name', 'email', 'country', 'city', 'street', 'house_number', 'supplier', 'debt_to_supplier', 'created_at')
    # Добавить фильтрацию по полям
    list_filter = ('city',)


# Зарегистрировать модель Product в панели администратора
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Отобразить в списке продуктов следующие поля
    list_display = ('name', 'model', 'realese_date')
