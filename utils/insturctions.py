INSTRUCTIONS = {
    'stroke': {
        'pattern': r'\{\{строка:(\w+):([^:]+):(\w+):(\w+)\}\}',
        'attrNames': ['name', 'placeholder', 'min', 'max']
    },
    'number': {
        'pattern': r'\{\{число:(\w+):([^:]+):(\w+):(\w+)\}\}',
        'attrNames': ['name', 'placeholder', 'min', 'max']
    },
    'logical': {
        'pattern': r'\{\{лог:(\w+):([^:]+)\}\}',
        'attrNames': ['name', 'placeholder']
    },
    'switcher': {
        'pattern': r'\{\{переключатель:(\w+):([^:]+):(\w+):(\w+)\}\}',
        'attrNames': ['name', 'placeholder', 'index', 'max']
    },
    'tables': {
        'pattern': r'\{\{таблица:(\w+):([^:]+):\[(.*?)\]\}\}',
        'attrNames': ['name', 'placeholder', 'fields']
    }
}
