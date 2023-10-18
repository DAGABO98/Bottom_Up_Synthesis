import traceback
import datetime
import optparse

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
        
        self.add_value(weight, value_type, value)
        return None

    
    def populate_arg_list(self, n, weight, arg_types):
        if n == 1:
            arg_list = []
            for expression in self.get_expressions_for_weight_and_type(weight, arg_types[0]):
                arg_list.append([expression])
        else:
            arg_list = []
            for curr_weight in range(1, weight-n+2):
                for expression in self.get_expressions_for_weight_and_type(curr_weight, arg_types[0]):
                    rest_of_expressions = self.populate_arg_list(n-1, weight-curr_weight, arg_types[1:])
                    for tail_expressions in rest_of_expressions:
                        arg_list.append([expression] + tail_expressions)
        
        return arg_list
    
    def execute_operation(self, op, args):
        arg_expressions = []
        arg_values = []

        for expression, value in args:
            arg_expressions.append(expression)
            arg_values.append(value)

        op_values = []
        for op_args in zip(*arg_values):
            op_value = self.dsl.execute_op(op, op_args)
            op_values.append(op_value)
        
        op_expression = (op, arg_expressions)
        return (op_expression, op_values)

    def synthesize(self, variable_names, input_examples, output_examples, weight_threshold=25):
        self.E = {}
        input_type = self.dsl.infer_types(input_examples)[0]
        output_type = self.dsl.infer_types(output_examples)[0]
        constant_values = self.dsl.extract_constants(input_examples, output_examples)

        input_values = []
        for variable_index, variable_name in enumerate(variable_names):
            inputs_for_examples = [input_examples[i][variable_index] for i in range(len(input_examples))]
            input_values.append((input_type[variable_index], (("input", variable_name), inputs_for_examples)))

        initial_values = constant_values + input_values
        for value_type, value in initial_values:
            weight = 1
            self.add_value(weight, value_type, value)
            
        for weight in range(2, weight_threshold):
            for op in self.dsl.valid_ops.values():
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

def run_synthesize(bustle, parser, variable_names, input_examples, 
                          output_examples, expected_output, test_num=1, weight_threshold=10):
    synthesized_expression = bustle.synthesize(variable_names=variable_names, 
                                               input_examples=input_examples, 
                                               output_examples=output_examples, 
                                               weight_threshold=weight_threshold)
    print("")
    print("Test " + str(test_num) + ": ")
    print("User provided variable names: " + str(variable_names))
    print("User provided input / output examples :")
    for i in range(len(input_examples)):
        print(str(input_examples[i]) + " -> " + str(output_examples[i]))
    print("Expected program: " + str(parser.generate_string_from_parse_tree(expected_output)))
    print("Generated program: " + str(parser.generate_string_from_parse_tree(synthesized_expression)))
    
    return synthesized_expression
    
def test_arithm_dsl():
    from arithm_dsl import Arithm_dsl
    from simple_dsl_parser import Simple_parser

    print("")
    print("Executing BUSTLE for Arithm DSL...")

    arithm_dsl = Arithm_dsl()
    arithm_bustle = Bustle(arithm_dsl)
    arithm_parser = Simple_parser(arithm_dsl)

    # Test 1
    variable_names1 = ["x", "y"]
    input_examples1 = [[2,3], [4,5]]
    output_examples1 = [6, 20]
    expected_output1 = ('mul', [('input', 'x'), ('input', 'y')])
    expression1 = run_synthesize(arithm_bustle, arithm_parser, variable_names1, input_examples1, 
                                 output_examples1, expected_output1, test_num=1)
    assert expression1 == expected_output1
    
    # Test 2
    variable_names2 = ["x", "y"]
    input_examples2 = [[2,4], [4,5]]
    output_examples2 = [-6, -9]
    expected_output2 = ('neg', [('add', [('input', 'x'), ('input', 'y')])])
    expression2 = run_synthesize(arithm_bustle, arithm_parser, variable_names2, input_examples2, 
                                 output_examples2, expected_output2, test_num=2)
    assert expression2 == expected_output2

    # Test 3
    variable_names3 = ["x", "y", "z"]
    input_examples3 = [[1, 3, 5], [7, 11, 13]]
    output_examples3 = [15, 1001]
    expected_output3 = ('mul', [('input', 'x'), ('mul', [('input', 'y'), ('input', 'z')])])
    expression3 = run_synthesize(arithm_bustle, arithm_parser, variable_names3, input_examples3, 
                                 output_examples3, expected_output3, test_num=3)
    assert expression3 == expected_output3

    # Test 4
    variable_names4 = ["x"]
    input_examples4 = [[5], [4], [3], [2], [1], [4], [5], [15]]
    output_examples4 = [1, 0, 0, 0, 0, 0, 1, 0]
    expected_output4 = ('mul', [('div', [5, ('input', 'x')]), ('div', [('input', 'x'), 5])])
    expression4 = run_synthesize(arithm_bustle, arithm_parser, variable_names4, input_examples4, 
                                 output_examples4, expected_output4, test_num=4)
    assert expression4 == expected_output4

    # Test 5
    variable_names5 = ["x"]
    input_examples5 = [[5], [4], [3], [2], [1], [0], [15]]
    output_examples5 = [5, 4, 3, 1, 1, 1, 15]
    expected_output5 = ('if', [('gt', [3, ('input', 'x')]), 1, ('input', 'x')])
    expression5 = run_synthesize(arithm_bustle, arithm_parser, variable_names5, input_examples5, 
                                 output_examples5, expected_output5, test_num=5)
    assert expression5 == expected_output5

    print("")
    print("The system passed all test cases for Arithm DSL!")

def test_string_dsl():
    from string_dsl import String_dsl
    from simple_dsl_parser import Simple_parser

    print("")
    print("Executing BUSTLE for String DSL...")

    string_dsl = String_dsl()
    string_bustle = Bustle(string_dsl)
    string_parser = Simple_parser(string_dsl)

    # Test 1
    variable_names1 = ["x"]
    input_examples1 = [["hello"], ["world"]]
    output_examples1 = ["h", "w"]
    expected_output1 = ('Left', [('input', 'x'), 1])
    expression1 = run_synthesize(string_bustle, string_parser, variable_names1, input_examples1, 
                                 output_examples1, expected_output1, test_num=1)
    assert expression1 == expected_output1

    # Test 2
    variable_names2 = ["x"]
    input_examples2 = [["hello"], ["world"]]
    output_examples2 = ["o", "d"]
    expected_output2 = ('Right', [('input', 'x'), 1])
    expression2 = run_synthesize(string_bustle, string_parser, variable_names2, input_examples2, 
                                 output_examples2, expected_output2, test_num=2)
    assert expression2 == expected_output2

    # Test 3
    variable_names3 = ["x", "y"]
    input_examples3 = [["hello", "you"], ["world", "domination"]]
    output_examples3 = ["helloyou", "worlddomination"]
    expected_output3 = ('Concatenate', [('input', 'x'), ('input', 'y')])
    expression3 = run_synthesize(string_bustle, string_parser, variable_names3, input_examples3, 
                                 output_examples3, expected_output3, test_num=3)
    assert expression3 == expected_output3

    # Test 4
    variable_names4 = ["x", "y"]
    input_examples4 = [["hello", "you"], ["world", "domination"]]
    output_examples4 = ["hello you", "world domination"]
    expected_output4 = ('Concatenate', [('input', 'x'), ('Concatenate', [' ', ('input', 'y')])])
    expression4 = run_synthesize(string_bustle, string_parser, variable_names4, input_examples4, 
                                 output_examples4, expected_output4, test_num=4)
    assert expression4 == expected_output4

    # Test 5
    variable_names5 = ["x"]
    input_examples5 = [["hello"], ["world"], ["domination"]]
    output_examples5 = ["ho", "wd", "dn"]
    expected_output5 = ('Concatenate', [('Left', [('input', 'x'), 1]), ('Right', [('input', 'x'), 1])])
    expression5 = run_synthesize(string_bustle, string_parser, variable_names5, input_examples5, 
                                 output_examples5, expected_output5, test_num=5)
    assert expression5 == expected_output5

    # Test 6
    variable_names6 = ["x"]
    input_examples6 = [["hello"], ["world"], ["domination"]]
    output_examples6 = ["xxxhello", "xxxworld", "xxxdomination"]
    expected_output6 = ('Concatenate', ['xxx', ('input', 'x')])
    expression6 = run_synthesize(string_bustle, string_parser, variable_names6, input_examples6, 
                                 output_examples6, expected_output6, test_num=6)
    assert expression6 == expected_output6

    # Test 7
    variable_names7 = ["x"]
    input_examples7 = [["abcdef"], ["abcxy"], ["abcop"]]
    output_examples7 = ["codef", "coxy", "coop"]
    expected_output7 = ('Substitute', [('input', 'x'), 'abc', 'co'])
    expression7 = run_synthesize(string_bustle, string_parser, variable_names7, input_examples7, 
                                 output_examples7, expected_output7, test_num=7)
    assert expression7 == expected_output7

    print("")
    print("The system passed all test cases for String DSL!")

def test():
    parser = optparse.OptionParser()
    parser.add_option("--mode", type=int, dest='mode', default=0, help='Select mode of operation.')

    (options, args) = parser.parse_args()

    if options.mode == 0:
        test_arithm_dsl()
    elif options.mode == 1:
        test_string_dsl()
    else:
        test_arithm_dsl()
        test_string_dsl()

if __name__ == "__main__":
    """Performs execution delta of the process."""
    print("Performing unit tests for BUSTLE")
    pStart = datetime.datetime.now()
    try:
        test()
    except Exception as errorMainContext:
        print("Fail End Process: ", errorMainContext)
        traceback.print_exc()
    qStop = datetime.datetime.now()
    print("Execution time: " + str(qStop-pStart))

