import string
from pprint import pprint


# recursive function to make a call in the most nested key of dictionary
# by using the list of keys
def dict_key_call(dictionary, keys):
    if len(keys) == 1:
        return dictionary[keys[0]]
    return dict_key_call(dictionary[keys[0]], keys[1:])


def optimize_data(template, data):
    new_dict = {}
    # templates in test are separated by newline \n, so i split them
    # also, because of this split last string will produce another one
    # which I exclude. I cant exclude last string if the template
    # consists only of 1 string, so i check this with
    # template_adjuster which is subtracted from templates
    template_adjuster = 0
    template_adjuster = 0 if len(template.split('\n')) == 1 else 1
    templates = template.split('\n')
    for i in range(len(templates) - template_adjuster):
        pieces = string.Formatter().parse(templates[i])
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
        # I get dict_keys from {languages[python][latest_version]}
        import re
        dict_keys = re.split('\W+', pieces_list[1])[:-1]

        # I make a new dict with nested dicts of keys
        # But the last key is not a dict itself, so i exclude it
        tmp_dict_nest = new_dict
        for key in dict_keys[:-1]:
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
