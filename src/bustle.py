class Bustle:
    def __init__(self, dsl):
        self.dsl = dsl
        self.E = {}
    
    def check_termination(self, value_type, output_type, value, output_examples):
        termination_flag = False
        if value_type == output_type:
            if value[1] == output_examples:
                termination_flag = True
        
        return termination_flag
    
    def check_containment(self, value, value_type):
        containment = False
        for weight_level_values in self.E.values():
            for curr_val in weight_level_values[value_type]:
                if value[1] == curr_val[1]:
                    containment = True
        
        return containment
    
    def get_value_expression(self, value):
        return value[0]
    
    def get_expressions_for_weight_and_type(self, weight, curr_type):
        return self.E.get(weight, {}).get(curr_type, [])
    
    def add_value(self, weight, value_type, value):
        if not self.check_containment(value, value_type):
            new_weight = weight

            if new_weight not in self.E:
                weight_level_dict = {}
                for available_type in self.dsl.valid_types:
                    weight_level_dict[available_type] = []
                self.E[new_weight] = weight_level_dict
            
            self.E[new_weight][value_type].append(value)
    
    def check_and_add_value(self, weight, value_type, output_type, value, output_examples):
        if self.check_termination(value_type, output_type, value, output_examples):
            return self.get_value_expression(value)
        
        self.add_value(self, weight, value_type, value)
        return None

    
    def populate_arg_list(self, n, weight, arg_types):
        if n == 1:
            arg_list = []
            for arg_type in arg_types:
                for expression in self.get_expressions_for_weight_and_type(weight, arg_type):
                    arg_list.append([expression])
        else:
            arg_list = []
            for curr_weight in range(1, weight-n+2):
                for arg_type in arg_types:
                    for expression in self.get_expressions_for_weight_and_type(curr_weight, arg_type):
                        rest_of_expressions = self.populate_arg_list(n-1, weight-curr_weight, arg_types)
                        for tail_expressions in rest_of_expressions:
                            arg_list.append([expression] + tail_expressions)
        
        return arg_list
    
    def execute_operation(self, op, args):
        arg_exprs = [expr for expr, _ in args]
        arg_vals = [val for _, val in args]

        values = []
        for op_args in zip(*arg_vals):
            op_value = self.dsl.execute_op(op, op_args)
            values.append(op_value)
        
        expression = (op, arg_exprs)
        return (expression, values)

    def predict(self, variable_names, input_examples, output_examples, weight_threshold=25):
        self.E = {}
        input_type = self.dsl.infer_types(input_examples)
        output_type = self.dsl.infer_types(output_examples)
        constant_values = self.dsl.extract_constants(input_examples, output_examples, input_type, output_type)

        input_values = []
        for input_example in input_examples:
            for variable_index, variable_name in enumerate(variable_names):
                inputs_for_examples = [input_example[variable_index] for _ in range(len(input_examples))]
                input_values.append((input_type[variable_index], (("input", variable_name), inputs_for_examples)))

        initial_values = constant_values + input_values
        for value_type, value in initial_values:
            weight = 1
            self.add_value(self, weight, value_type, value)
            
        for weight in range(2, weight_threshold):
            for op in self.dsl.valid_ops:
                n = self.dsl.get_op_arity(op)
                value_type = self.dsl.get_op_return_type(op)
                arg_types = self.dsl.get_op_arg_types(op)

                potential_args = self.populate_arg_list(n, weight, arg_types)
                for args in potential_args:
                    try:
                        value = self.execute_operation(op, args)
                    except:
                        continue

                    expression = self.check_and_add_value(weight, value_type, output_type, value, output_examples)
                    if expression is None:
                        continue
                    else:
                        return expression
        
        return self.E

