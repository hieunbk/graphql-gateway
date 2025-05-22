from datetime import date
from typing import Union

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import or_
from sqlalchemy.orm import Query
from sqlalchemy.sql import Select


class AbstractFilter(Filter):
    class Constants(Filter.Constants):
        ...
        # custom_fields_in_ornull = [
        #     "gender__in",
        # ]
        # Define method to filter (filter_{name})
        # Example: _filter_person_geo
        # custom_field_method = [
        #     "person_geo",
        # ]

    @property
    def filtering_fields(self):
        fields = self.model_dump(
            exclude_none=True, exclude_unset=True, exclude=self.Constants.custom_fields_in_ornull
        )
        fields.pop(self.Constants.ordering_field_name, None)
        _ = [fields.pop(field, None) for field in self.Constants.custom_field_method]
        return fields.items()

    def _filter_custom_fields_in_ornull(self, query: Union[Query, Select], null_value="null"):
        opr_in, opr_isnull = "in_", "is_"

        fields_in_ornull = self.model_dump(
            exclude_none=True, exclude_unset=True, include=self.Constants.custom_fields_in_ornull
        )
        for field_name, value in fields_in_ornull.items():
            field_name, operator, _value = (
                field_name.split("__")[0],
                opr_in,
                [v for v in value if v],
            )

            model_field = getattr(self.Constants.model, field_name)
            filters = [getattr(model_field, operator)(_value)]
            if null_value in value:
                filters.append(getattr(model_field, opr_isnull)(None))
            query = query.filter(or_(*filters))
        return query

    def _filter_methods(self, query: Union[Query, Select]):
        # call all method in custom_field_method
        filters_keys = self.model_dump(exclude_none=True, exclude_unset=True).keys()
        custom_fields = [f for f in self.Constants.custom_field_method if f in filters_keys]
        for filter_field in custom_fields:
            query = getattr(self, f"filter_{filter_field}")(
                query, filter_field, getattr(self, filter_field)
            )
        return query

    def filter(self, query: Union[Query, Select]):
        query = self._filter_methods(query)
        query = self._filter_custom_fields_in_ornull(query)
        query = super().filter(query)
        return query

    def to_db(self) -> dict:
        value = self.model_dump(mode="json", exclude_unset=True, exclude_none=True)
        value_converted = {}
        for k, v in value.items():
            if isinstance(v, date):
                v = v.isoformat()
            if isinstance(v, list):
                v = ",".join([str(_v) for _v in v])
            value_converted[k] = v
        return value_converted
