from decimal import Decimal

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

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
    list_display = ('type', 'name', 'email', 'country', 'city', 'street', 'house_number', 'supplier_link', 'debt_to_supplier', 'created_at')
    # Добавить фильтрацию по полям
    list_filter = ('city',)

    # Добавить действие для обнуления задолженности перед поставщиком
    actions = ('clear_debt_to_supplier', 'clear_debt_to_suppliers')
    # Кастомизировать шаблон формы редактирования объекта
    # Опредедить путь к HTML-шаблону, который будет использоваться вместо стандартного шаблона формы редактирования
    change_form_template = 'admin/network_participant_change_form.html'

    def supplier_link(self, obj):
        '''
        Возвращает ссылку на страницу редактирования поставщика
        :param obj:
        :return:
        '''
        # Проверить наличие поставщика
        if obj.supplier:
            url = reverse('admin:distribution_network_networkparticipant_change', args=(obj.supplier.id,))
            return format_html('<a href="{}">{}</a>', url, obj.supplier)
        # Если поставщика нет, вернуть прочерк
        return '-'

    def clear_debt_to_supplier(self, request, object_id):
        '''
        Обнуляет поле debt_to_supplier у одного объекта
        :param request: объект HTTP-запроса
        :param object_id: ID объекта, который нужно изменить
        :return:
        '''
        # Получить объект
        obj = self.get_object(request, object_id)
        # Обнулить поле debt_to_supplier
        obj.debt_to_supplier = Decimal('0.00')
        # Сохранить изменения
        obj.save()
        # Показать сообщение
        self.message_user(request, 'Задолженность обнулена', messages.SUCCESS)
        # Вернуться назад
        return HttpResponseRedirect('../')

    def clear_debt_to_suppliers(self, request, queryset):
        '''
        Обнуляет поле debt_to_supplier у выбранных объектов
        :param request: объект HTTP-запроса
        :param queryset: набор выбранных объектов, которые нужно изменить
        :return:
        '''
        # Массовое обновление поля debt_to_supplier
        updated = queryset.update(debt_to_supplier=Decimal('0.00'))
        # Показать сообщение
        self.message_user(request,f'Задолженность обнулена у {updated} участников', messages.SUCCESS)
    # Задать понятное название для выпадающего мень действий
    clear_debt_to_suppliers.short_description = 'Обнулить задолженность у выбранных участников'


    # Добавить url-адрес для обнуления поля debt_to_supplier к стандартным маршрутам админки
    def get_urls(self):
        # Вызвать метод get_urls родительского класса (Получить стандартные URL)
        urls = super().get_urls()
        # Связать URL с обработчиком
        custom_urls = [
            path('<int:object_id>/clear_debt/', self.admin_site.admin_view(self.clear_debt_to_supplier), name='clear_debt_to_supplier'),
        ]
        # Вернуть объединение двух списков URL-паттернов
        return custom_urls + urls


# Зарегистрировать модель Product в панели администратора
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Отобразить в списке продуктов следующие поля
    list_display = ('name', 'model', 'realese_date')
