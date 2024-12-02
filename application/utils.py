def get_root_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
        client_ip = ip_list[0]  # Берём первый IP из списка
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip


