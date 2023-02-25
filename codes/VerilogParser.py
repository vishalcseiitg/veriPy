import re

class VerilogParser:
    def __init__(self):
        self.module_name = None
        self.input_ports = []
        self.output_ports = []
        self.internal_wires = []

    def parse_module(self, code):
        # Find module definition
        match = re.search(r"module\s+(\w+)\s*\((.*?)\)\s*;", code, re.DOTALL)
        if not match:
            raise ValueError("Module definition not found")
        self.module_name = match.group(1)
        port_decls = match.group(2)

        # Parse input ports
        match = re.findall(r"input\s+(.*?)[,;\n]", port_decls)
        self.input_ports = [p.strip() for p in match]

        # Parse output ports
        match = re.findall(r"output\s+(.*?)[,;\n]", port_decls)
        self.output_ports = [p.strip() for p in match]

        # Parse internal wires
        match = re.findall(r"wire\s+(.*?)[,;\n]", code)
        self.internal_wires = [w.strip() for w in match]

        # TODO: Parse other constructs like assignments and functions
        
       
code = """
module adder(input a, input b, output s);
  wire c;
  assign {s,c} = a + b;
endmodule
"""

parser = VerilogParser()
parser.parse_module(code)

print(parser.module_name)  # "adder"
print(parser.input_ports)  # ["a", "b"]
print(parser.output_ports)  # ["s"]
print(parser.internal_wires)  # ["c"]

#############################################################################################

#output                      adder
                          ['a', 'b']
                            ['s']
                            ['c']

#############################################################################################
