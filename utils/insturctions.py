INSTRUCTIONS = {
    'stroke': {
        'pattern': r'\{\{строка:(\w+):([^:]+):(\w+):(\w+)\}\}',
        'attrNames': ['name', 'placeholder', 'min', 'max']
    },
    'alt_stroke': {
        'pattern': r'\{\{([^:{}]+)\}\}',
        'attrNames': ['placeholder'],
        'parrentName': 'stroke'
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

TYPES = {
    'stroke': 'строка',
    'number': 'число',
    'logical': 'лог',
    'switcher': 'переключатель',
    'tables': 'таблица'
}

DEFAULT_VALUES = {
    'name': 'None',
    'placeholder': 'None',
    'min': 0,
    'max': 10000000,
    'index': 0,
    'fileds': []
}