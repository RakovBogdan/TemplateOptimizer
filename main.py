import string
from pprint import pprint


# recursive function to make a call in the most nested key of dictionary
# by using the list of keys
def dict_key_call(dictionary, keys):
    if len(keys) == 1:
        return dictionary[keys[0]]
    return dict_key_call(dictionary[keys[0]], keys[1:])


def optimize_data(template, data):
    pieces = string.Formatter().parse(template)
    # pieces are result of Formatter.parse, which,
    # according to python docs is an iterable of tuples
    # I traverse iterable and then every tuple of len = 1
    # to collect them into single list
    pieces_list = []
    for pieces_tuple in pieces:
        for piece in pieces_tuple:
            pieces_list.append(piece)
    # pieces_list[0] has 'Python version:'
    # and pieces_list[1] has {languages[python][latest_version]}
    # + weird empty string in the end, so i get rid of this with [:-1]
    # dict_keys is the keys that I get from {languages[python][latest_version]}
    import re
    dict_keys = re.split('\W+', pieces_list[1])[:-1]

    # I make a new dict with nested dicts of keys
    new_dict = {}
    tmp_dict_nest = new_dict
    for key in dict_keys:
        if key not in tmp_dict_nest:
            tmp_dict_nest[key] = {}
        tmp_dict_nest = tmp_dict_nest[key]

    # now I assign to the most nested dict a value from data
    # with usage of recursive helper fucntion to call the parameter
    # from a list of keys
    value = dict_key_call(data, dict_keys)
    tmp_dict_nest[dict_keys[-1]] = value
    return new_dict


def main():
    template = 'Python version: {languages[python][latest_version]}'
    data = {
        'languages': {
            'python': {
                'latest_version': '3.6',
                'site': 'http://python.org',
            },
            'rust': {
                'latest_version': '1.17',
                'site': 'https://rust-lang.org',
            },
        },
    }
    print("Original data:")
    pprint(data)

    new_data = optimize_data(template, data)
    print("Optimized data:")
    pprint(new_data)


if __name__ == '__main__':
    main()
