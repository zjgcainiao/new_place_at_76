
from .base import formset_factory
from .reapair_order_update import RepairOrderUpdateForm

RepairOrderFormset = formset_factory(RepairOrderUpdateForm, extra=0)