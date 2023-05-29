# procesador.py

from obj_parser import Obj_Parser

def main():
    print("hi")
    objParser = Obj_Parser(obj_dir="./ovejota.obj")
    cuads, dir_funcs, consts = objParser.parse()
    print(cuads, dir_funcs, consts)



if __name__ == "__main__":
    main()