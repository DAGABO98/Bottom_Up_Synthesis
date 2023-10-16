class String_dsl:

    def __init__(self):
        self.valid_ops = self.initialize_ops()
        self.valid_types = ["int", "bool", "str"]

    def initialize_ops(self):
        op_dict = {}
        deafult_ops = ["Concatenate", "Left", "Right", "Replace", "Trim", "Repeat", "Substitute", 
                       "SubstituteI", "ToText", "LowerCase", "UpperCase", "ProperCase", 
                       "Equals", "Len", "If"]
        for op in deafult_ops:
            op_dict[op.lower()] = op
        
        return op_dict
    
    def is_valid_op(self, token):
        return token.lower() in self.valid_ops
    
    def obtain_op_name(self, token):
        return self.valid_ops[token.lower()]
    
    def get_op_types(self, op):
        if op == "Concatenate":
            return ("str", ("str", "str"))
        elif op == "Left":
            return ("str", ("str", "str"))
        elif op == "Right":
            return ("str", ("str", "str"))
        elif op == "Replace":
            return ("str", ("str", "str"))
        elif op == "Trim":
            return ("str", ("str", "str"))
        elif op == "Repeat":
            return ("str", ("str", "str"))
        elif op == "Substitute":
            return ("str", ("str", "str"))
        elif op == "SubstituteI":
            return ("str", ("str", "str"))
        elif op == "ToText":
            return ("str", ("str", "str"))
        elif op == "LowerCase":
            return ("str", ("str", "str"))
        elif op == "UpperCase":
            return ("str", ("str", "str"))
        elif op == "ProperCase":
            return ("str", ("str", "str"))
        elif op == "Equals":
            return ("str", ("str", "str"))
        elif op == "Len":
            return ("str", ("str", "str"))
        elif op == "Add":
            return 0
        elif op == "Multiply":
            return 0
        elif op == "Subtract":
            return 0
        elif op == "Divide":
            return 0
        elif op == "If":
            return ("str", ("str", "str"))
        else:
            assert False, "Invalid operator " + str(op)
    
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
        elif op == "SubstituteI":
            return args[0].replace(args[1], args[2], args[3])
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
    
    def extract_constants(self, input_examples, output_examples, input_type, output_type):
        default_constants = [0, 1, 2, 3, 5, 7, 11] #prime numbers
        int_constant_list = []
        for constant_value in default_constants:
            constants_for_examples = [constant_value for _ in range(len(input_examples))]
            int_constant_list.append(("int", (constant_value, constants_for_examples)))
        
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