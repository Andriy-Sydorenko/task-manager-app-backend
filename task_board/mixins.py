class FilterMixin:
    def filter_queryset(self, queryset):
        params = self.request.query_params
        name = params.get("name")
        description = params.get("description")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if description:
            queryset = queryset.filter(description__icontains=description)
        return queryset.filter(created_by=self.request.user)
