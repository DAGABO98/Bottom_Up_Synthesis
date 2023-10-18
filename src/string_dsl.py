import difflib

class String_dsl:

    def __init__(self):
        self.valid_ops = self.initialize_ops()
        self.valid_types = ["int", "bool", "str"]

    def initialize_ops(self):
        op_dict = {}
        deafult_ops = ["Concatenate", "Left", "Right", "Replace", "Trim", "Repeat", "Substitute", 
                       "ToText", "LowerCase", "UpperCase", "ProperCase", "Equals", "Lt", "Gt", 
                       "Len", "If"]
        for op in deafult_ops:
            op_dict[op.lower()] = op
        
        return op_dict
    
    def is_valid_op(self, token):
        return token.lower() in self.valid_ops
    
    def obtain_op_name(self, token):
        return self.valid_ops[token.lower()]
    
    def get_op_types(self, op):
        if op == "Concatenate":
            op_type = "str"
            arg_type = ("str", "str")
        elif op in ["Left", "Right"]:
            op_type = "str"
            arg_type = ("str", "int")
        elif op == "Replace":
            op_type = "str"
            arg_type = ("str", "int", "int", "str")
        elif op == "Trim":
            op_type = "str"
            arg_type = ("str", )
        elif op == "Repeat":
            op_type = "str"
            arg_type = ("str", "int")
        elif op == "Substitute":
            op_type = "str"
            arg_type = ("str", "str", "str")
        elif op == "ToText":
            op_type = "str"
            arg_type = ("int",)
        elif op in ["LowerCase", "UpperCase", "ProperCase"]:
            op_type = "str"
            arg_type = ("str",)
        elif op in ["Equals", "Lt", "Gt"]:
            op_type = "bool"
            arg_type = ("int", "int")
        elif op == "Len":
            op_type = "int"
            arg_type = ("str",)
        elif op in ["Add", "Multiply", "Subtract", "Divide"]:
            op_type = "int"
            arg_type = ("int", "int")
        elif op == "If":
            op_type = "str"
            arg_type = ("bool", "str", "str")
        else:
            assert False, "Invalid operator " + str(op)
        
        return (op_type, arg_type)
    
    def get_op_arg_types(self, op):
        _, arg_types = self.get_op_types(op)
        return arg_types
    
    def get_op_return_type(self, op):
        return_type, _ = self.get_op_types(op)
        return return_type
    
    def get_op_arity(self, op):
        op_arity = len(self.get_op_arg_types(op))
        return op_arity 
    
    def execute_op(self, op, args):
        if op == "Concatenate":
            return args[0] + args[1]
        elif op == "Left":
            return args[0][:args[1]]
        elif op == "Right":
            return args[0][len(args[0])-args[1]:]
        elif op == "Replace":
            init_str = args[0]
            start = args[1]
            length = args[2]
            replacement = args[3]
            new_string = init_str[:start] + replacement + init_str[start+length:]
            return new_string
        elif op == "Trim":
            return args[0].trim()
        elif op == "Repeat":
            return args[0] * args[1]
        elif op == "Substitute":
            return args[0].replace(args[1], args[2])
        elif op == "ToText":
            return str(args[0])
        elif op == "LowerCase":
            return args[0].lower()
        elif op == "UpperCase":
            return args[0].upper()
        elif op == "ProperCase":
            return args[0].title()
        elif op == "Equals":
            return args[0] == args[1]
        elif op == "Lt":
            return args[0] < args[1]
        elif op == "Gt":
            return args[0] > args[1]
        elif op == "Len":
            return len(args[0])
        elif op == "Add":
            return args[0] + args[1]
        elif op == "Multiply":
            return args[0] * args[1]
        elif op == "Subtract":
            return args[0] - args[1]
        elif op == "Divide":
            return args[0] // args[1]
        elif op == "If":
            if args[0]:
                return args[1]
            else:
                return args[2]
        else:
            assert False, "Invalid operator " + str(op)
    
    def evaluate_parse_tree(self, parse_tree, input_dict):
        if type(parse_tree) is tuple or type(parse_tree) is list:
            if parse_tree[0] == "input":
                return input_dict[parse_tree[1]]
            else:
                evaluated_args = [self.evaluate_parse_tree(arg_tree, input_dict) for arg_tree in parse_tree[1]]
                return self.execute_op(parse_tree[0], evaluated_args)
        else:
            return parse_tree
    
    def _get_string_overlap(self, example1, example2):
        seq_match = difflib.SequenceMatcher(None, example1, example2)
        pos_a, _, size = seq_match.find_longest_match(0, len(example1), 0, len(example2))
        return example1[pos_a: pos_a+size]
    
    def _get_max_output_overlap(self, output_examples):
        max_output_match = ""
        for output_index in range(len(output_examples)-1):
            if type(output_examples[output_index]) is str:
                if output_index == 0:
                    max_output_match = self._get_string_overlap(output_examples[output_index], output_examples[output_index+1])
                else:
                    max_output_match = self._get_string_overlap(max_output_match, output_examples[output_index+1])
            else:
                continue
        
        return max_output_match
    
    def _get_max_input_overlap(self, input_examples):
        max_input_match = ""
        for input_index in range(len(input_examples)-1):
            if len(input_examples[input_index]) == 1:
                if input_index == 0:
                    max_input_match = self._get_string_overlap(input_examples[input_index][0], input_examples[input_index+1][0])
                else:
                    max_input_match = self._get_string_overlap(max_input_match, input_examples[input_index+1][0])
            else:
                for i in range(len(input_examples[input_index])-1):
                    if input_index == 0 and input_index == 0:
                        max_input_match = self._get_string_overlap(input_examples[input_index][i], input_examples[input_index][i+1])
                    else:
                        max_input_match = self._get_string_overlap(max_input_match, input_examples[input_index][i+1])
                
                for i in range(len(input_examples[input_index+1])):
                    max_input_match = self._get_string_overlap(max_input_match, input_examples[input_index+1][i])
        
        return max_input_match
    
    def extract_constants(self, input_examples, output_examples):
        int_constants = [0, 1, 2]
        int_constant_list = []
        for constant_value in int_constants:
            constants_for_examples = [constant_value for _ in range(len(input_examples))]
            int_constant_list.append(("int", (constant_value, constants_for_examples)))

        max_output_match = self._get_max_output_overlap(output_examples)
        max_output_match_set = set(max_output_match)

        max_input_match = self._get_max_input_overlap(input_examples)
        max_input_match_set = set(max_input_match)

        default_str_constants = [" ", ",", ":"]

        str_constant_set = max_output_match_set | max_input_match_set

        IO_str_constants = []
        for str_constant in str_constant_set:
            IO_str_constants.append(str_constant)
        
        IO_str_constants.append(max_input_match)
        IO_str_constants.append(max_output_match)

        str_constants = default_str_constants + IO_str_constants
        
        str_constant_list = []
        for string_constant in str_constants:
            constants_for_examples = [string_constant for _ in range(len(input_examples))]
            str_constant_list.append(("str", (string_constant, constants_for_examples)))

        constant_list = int_constant_list + str_constant_list
        return constant_list
    
    def _infer_types(self, example):
        if type(example) is list:
            type_list = []
            for element in example:
                elem_type = self._infer_types(element)
                type_list.append(elem_type)
            return type_list
        elif type(example) is str:
            return "str"
        elif type(example) is int:
            return "int"
        elif type(example) is bool:
            return "bool"
        else:
            assert False, "no type found for " + str(example)
                
    
    def infer_types(self, examples):
        example_types = []
        for example in examples:
            ex_type = self._infer_types(example)
            example_types.append(ex_type)
        
        return example_types