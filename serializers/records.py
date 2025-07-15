def records_serializer(queryset):
    """
    Converts the queryset to the required list format
    """
    formatted_data = []
    for record in queryset:
        formatted_record = [
            record[0],  # id
            record[1] or '',  # description
            record[2].strftime('%Y-%m-%d') if record[2] else '',  # date
            record[3] or '',  # category
            str(record[4]) if record[4] else '',  # amount
            record[5] or ''   # source
        ]
        formatted_data.append(formatted_record)
    return formatted_data
