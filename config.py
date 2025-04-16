import ast

class ConfigTXT:
    def __init__(self, list, file:str|None="configs.txt"):
        '''
        Class to manage settings, which are changed via text editor by the user

        List template: {"option":"type,default_value"}

        Types: "str","literal","int"
        '''
        self.params = {};
        while True:
            try:
                with open(file, "r") as config:
                    for c in config.readlines():
                        def get_split(mode:str|None=None):
                            '''
                            ***mode***: "literal" or "int"
                            '''
                            if mode is None or mode == "str":
                                var = c.split("=")[1].split(",")[0];
                            match mode:
                                case "literal":
                                    var = ast.literal_eval(c.split("=")[1].split(",")[0]);
                                case "int":
                                    var = int(c.split("=")[1].split(",")[0]);
                            return var;
                        for i in list:
                            if c.split("=")[0] == i:
                                self.params[i] = get_split(list.get(i).split(",")[0]);
                break;
            except:
                with open(file, "w") as config:
                    for i in list:
                        config.write(f"{i}={list.get(i).split(",")[1]},\n");

    def get(self, param):
        return self.params.get(param);