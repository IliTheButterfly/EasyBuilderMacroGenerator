from __future__ import annotations
from typing import Callable, Dict, List, Tuple
from pdfminer.high_level import extract_text
from argparse import ArgumentParser, _SubParsersAction, Namespace
from re import fullmatch

commands:List[Tuple[Callable[[_SubParsersAction]], Callable[[Namespace]]]] = []

def command(args_builder:Callable[[_SubParsersAction]]) -> Callable[[Callable[[Namespace]]], Callable[[Namespace]]]:
    def predicate(cmd:Callable[[Namespace]]) -> Callable[[Namespace]]:
        commands.append((args_builder, cmd))
        return cmd
    return predicate

# Extract pdf to file
def extract_pdf_args(parser:_SubParsersAction):
    p:ArgumentParser = parser.add_parser("extract_pdf", help="Extract text from the weintek manual")
    p.add_argument("infile", help="Input pdf file")
    p.add_argument("outfile", help="Output text file")
    
def extract_pdf_logic(infile:str) -> str:
    pdf_file = infile
    return extract_text(pdf_file)
    
@command(extract_pdf_args)
def extract_pdf(args:Namespace):
    text = extract_pdf_logic(args.infile)
    
    with open(args.outfile, "w") as wr:
        wr.write(text)

# Extract instruction names
def extract_names_args(parser:_SubParsersAction):
    p:ArgumentParser = parser.add_parser("extract_names", help="Extract instruction names from text")
    p.add_argument("infile", help="Input pdf file")
    p.add_argument("outfile", help="Output text file")
    
def extract_names_logic(intext:str) -> List[str]:
    start = intext.find("18.7.1.")
    end = intext.find("18.7.2.")
    text = intext[start:end]
    
    lines = text.splitlines()
    def find_names(line:str) -> bool:
        if not line.strip().isalnum():
            return False
        if not len(line.strip().split(' ')) == 1:
            return False
        if not line.endswith(" "):
            return False
        if line.strip() in ["Description"]:
            return False
        if "." in line:
            return False
        return True
            
    lines = filter(find_names, lines)
    
    return [line.strip() for line in lines]
    
@command(extract_names_args)
def extract_names(args:Namespace):
    with open(args.infile, "r") as rd:
        names = extract_names_logic(rd.read())
    
    with open(args.outfile, "w") as wr:
        wr.write("\n".join(names))
        
# Extract help from instructions
def extract_help_args(parser:_SubParsersAction):
    p:ArgumentParser = parser.add_parser("extract_help", help="Extracts help from the weintek manual")
    p.add_argument("manual_file", help="Path to extracted text from the manual")
    p.add_argument("names_file", help="Path to the instruction names")
    p.add_argument("outfile", help="Output file")
    
def extract_help_logic(manual_text:str, instruction_names:List[str]) -> Dict[str, str]:
    start = manual_text.find("18.7.2.")
    end = manual_text.find("18.8.1.")
    lines = manual_text[start:end].splitlines()
    
    current_instruction = ""
    current_help = ""
    
    res:Dict[str, str] = {}
    for line in lines:
        if line == " ":
            continue
        if line.startswith("EasyBuilder"):
            continue
        if line.strip() in ["Syntax", "18.8.1.", "18.7.2.", "Device"]:
            continue
        if "Macro Reference" in line:
            continue
        if line.strip() == "Name":
            if current_instruction != "":
                current_help = current_help.replace("\n\n\n", "\n")
                res[current_instruction] = current_help
            current_help = ""
            continue
        if fullmatch("\\d\\d-\\d\\d", line.strip()):
            continue
        if line.strip() in instruction_names:
            current_instruction = line.strip()
            continue
        current_help += line.strip() + "\n"
    
    return res

@command(extract_help_args)
def extract_help(args:Namespace):
    with open(args.manual_file, "r") as rd:
        manual = rd.read()
    with open(args.names_file, "r") as rd:
        names = [line.strip() for line in rd.readlines()]
    
    out = extract_help_logic(manual, names)
    
    with open(args.outfile, "w") as wr:
        for name, help in out.items():
            print("{{" + name + "}}", file=wr)
            print(help, file=wr)

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Build parser
    for builder, _ in commands:
        builder(subparsers)
    
    args = parser.parse_args()

    for _, cmd in commands:
        if cmd.__name__ == args.command:
            cmd(args)

if __name__ == "__main__":
    main()