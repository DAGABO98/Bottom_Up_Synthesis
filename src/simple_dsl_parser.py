import io
import tokenize

class Simple_parser:

    def __init__(self, dsl):
        self.dsl = dsl
    
    def get_tokens(self, input_string):
        tokens_iter = tokenize.generate_tokens(io.StringIO(input_string).readline)
        token_list = [token.string for token in tokens_iter if token.string != ""]
        return token_list
    
    def generate_parse_tree(self, tokens, current_index=0):
        if self.dsl.is_valid_op(tokens[current_index]):
            op = self.dsl.obtain_op_name(tokens[current_index])
            return_type, arg_types = self.dsl.get_op_types(op)

            # Check valid syntax of operation call
            current_index += 1
            assert tokens[current_index] == "("
            current_index += 1

            num_args = len(arg_types)
            args = []
            
            for arg_index in range(num_args):
                arg_parse_tree, current_index = self.generate_parse_tree(tokens=tokens, 
                                                                         current_index=current_index)
                args.append(arg_parse_tree)

                if tokens[current_index] == ",":
                    current_index += 1
            
            assert tokens[current_index] == ")"
            return ((op, args), current_index)
        
        elif tokens[current_index][0].isalpha():
            var_name = tokens[current_index]
            current_index += 1
            identifier_complete = False

            while not identifier_complete:
                if tokens[current_index] == ",":
                    identifier_complete = True
                else:
                    var_name += tokens[current_index]
                    current_index += 1

            return (("input", var_name), current_index)
        
        elif tokens[current_index].startswith('"'):
            string_value = tokens[current_index][1:-1]
            current_index += 1
            return (string_value, current_index)
        
        else:
            if tokens[current_index] == "-" and tokens[current_index+1].isnumeric():
                current_index += 1
                integer_comp = int(tokens[current_index])
                current_index += 1
                return (-1*integer_comp, current_index)
            elif tokens[current_index].isnumeric():
                integer_comp = int(tokens[current_index])
                current_index += 1
                return (integer_comp, current_index)
            else:
                assert False, "invalid token " + str(tokens[current_index])

    
    def parse_input(self, input_string):
        input_tokens = self.get_tokens(input_string)
        parse_tree, current_index = self.generate_parse_tree(input_tokens)

        # Check consistency of the index with the length of the tokens
        assert current_index == len(input_tokens)

        return parse_tree
    
    def generate_string_from_parse_tree(self, parse_tree):
        if type(parse_tree) is tuple or type(parse_tree) is list:
            if parse_tree[0] == "input":
                return str(parse_tree[1])
            else:
                return parse_tree[0] + "(" + ", ".join([self.generate_string_from_parse_tree(arg_tree) for arg_tree in parse_tree[1]]) + ")"
        elif type(parse_tree) is str:
            return '"' + parse_tree +'"'
        elif type(parse_tree) is int:
            return str(parse_tree)
        else:
            assert False, "invalid parse tree " + str(parse_tree)
            



