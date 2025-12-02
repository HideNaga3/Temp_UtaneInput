class CollationTwoText:
    def collation_two_text(self, new_text, ver_text):
        new_len = len(new_text)
        ver_len = len(ver_text)
        if new_text == ver_text:
            return None
        text_len = new_len if new_len > ver_len else ver_len
        invalid_dict = {
                'normal': {
                        'new': {'char': None, 'index': None},
                        'ver': {'char': None, 'index': None},
                },
                'rev':{
                        'new': {'char': None, 'index': None},
                        'ver': {'char': None, 'index': None},
                }
        }

        for i in range(text_len):
            try:
                if new_text[i] != ver_text[i]:
                    invalid_dict['normal'] = {
                            'new': {'index': i, 'char': new_text[i]},
                            'ver': {'index': i, 'char': ver_text[i]}
                    }
                    break
            except:
                break
        new_rev = new_text[::-1]
        ver_rev = ver_text[::-1]
        for i in range(text_len):
            new_index = len(new_text) - 1 - i
            ver_index = len(ver_text) - 1 - i
            try:
                if new_rev[i] != ver_rev[i]:
                    invalid_dict['rev'] = {
                            'new': {'index': new_index, 'char': new_rev[i]},
                            'ver': {'index': ver_index, 'char': ver_rev[i]}
                    }
                    break
            except Exception as e:
                break
        new_set = set(new_text)
        ver_set = set(ver_text)
        new_diff = ver_set - new_set
        ver_diff = new_set - ver_set
        invalids = []
        if invalid_dict['normal'] == invalid_dict['rev'] or invalid_dict['rev']['ver']['char'] is None or invalid_dict['rev']['new']['index'] is None:
            invalids = [invalid_dict['normal']]
        else:
            invalids = [invalid_dict['normal'], invalid_dict['rev']]
        result_dict = {'normal_and_rev': invalids, 'new_diff': new_diff, 'ver_diff': ver_diff}
        return result_dict

if __name__ == '__main__':
    collation_test = CollationTwoText()
    result_dict = collation_test.collation_two_text('あいうえおか聞く', 'あいかおきさく')
    print(result_dict)