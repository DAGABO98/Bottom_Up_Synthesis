class Arithm_dsl:

    def __init__(self):
        self.valid_ops = self.initialize_ops()
        self.valid_types = ["int", "bool"]

    def initialize_ops(self):
        op_dict = {}
        deafult_ops = ["add", "sub", "mul", "div", "neg", "eq", "gt", "lt", "max", "min", "if"]
        for op in deafult_ops:
            op_dict[op.lower()] = op
        
        return op_dict
    
    def is_valid_op(self, token):
        return token.lower() in self.valid_ops
    
    def obtain_op_name(self, token):
        return self.valid_ops[token.lower()]
    
    def get_op_types(self, op):
        if op in ["add", "sub", "mul", "div", "max", "min"]:
            op_type = "int"
            arg_type = ("int", "int")
        elif op in ["neg"]:
            op_type = "int"
            arg_type = ("int",)
        elif op in ["eq", "gt", "lt"]:
            op_type = "bool"
            arg_type = ("int", "int")
        elif op in ["if"]:
            op_type = "int"
            arg_type = ("bool", "int", "int")
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
        if op == "add":
            return args[0] + args[1]
        elif op == "sub":
            return args[0] - args[1]
        elif op == "mul":
            return args[0] * args[1]
        elif op == "div":
            return args[0] // args[1]
        elif op == "neg":
            return -1*args[0]
        elif op == "eq":
            return args[0] == args[1]
        elif op == "gt":
            return args[0] > args[1]
        elif op == "lt":
            return args[0] < args[1]
        elif op == "max":
            return max(args[0], args[1])
        elif op == "min":
            return min(args[0], args[1])
        elif op == "if":
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
    
    def extract_constants(self, input_examples, output_examples):
        default_constants = [0, 1, 2, 3, 5, 7, 11] 
        constant_list = []
        for constant_value in default_constants:
            constants_for_examples = [constant_value for _ in range(len(input_examples))]
            constant_list.append(("int", (constant_value, constants_for_examples)))
        
        return constant_list
    
    def _infer_types(self, example):
        if type(example) is list:
            type_list = []
            for element in example:
                elem_type = self._infer_types(element)
                type_list.append(elem_type)
            return type_list
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
