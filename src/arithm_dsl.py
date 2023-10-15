
class Arithm_dsl:

    def __init__(self):
        self.valid_ops = self.initialize_ops()
        self.valid_types = ["int", "bool"]

    def initialize_ops(self):
        op_dict = {}
        deafult_ops = ["add", "sub", "mul", "div", "neg", "eq", "gt", "lt"]
        for op in deafult_ops:
            op_dict[op.lower()] = op
        
        return op_dict
    
    def is_valid_op(self, token):
        return token.lower() in self.valid_ops
    
    def obtain_op_name(self, token):
        return self.valid_ops[token.lower()]
    
    def get_op_types(self, op):
        if op in ["add", "sub", "mul", "div"]:
            return ("int", ("int", "int"))
        elif op in ["neg"]:
            return ("int", ("int",))
        elif op in ["eq", "gt", "lt"]:
            return ("bool", ("int", "int"))
        elif op in ["if"]:
            return ("int", ("bool", "int", "int"))
        else:
            assert False, "Invalid operator " + str(op)
    
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
