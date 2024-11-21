configs = {}


def read_config(file_path='./config/application.properties'):
    if configs:
        return configs
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    pairs = [line.strip().split('=', 1) for line in content.splitlines() if '=' in line]
    result_dict = {key.strip(): value.strip() for key, value in pairs}
    configs.update(result_dict)
    print(f'application.properties: {configs}')
    return configs


if __name__ == '__main__':
    read_config()
