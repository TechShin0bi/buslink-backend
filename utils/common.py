def logo_thumbnail(self, obj):
    if obj.agency_logo:
        return format_html(
            '<a href="{}" target="_blank">'
            '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />'
            '</a>',
            obj.agency_logo.url,
            obj.agency_logo.url
        )
    return "-"