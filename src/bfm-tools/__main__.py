#****************************************************************************
#* 
#****************************************************************************
import argparse
import os
import json
from string import Template

def load_template_files(template_dir, prefix):
    templates = {}
    
    for file in os.listdir(template_dir):
        if os.path.isdir(os.path.join(template_dir, file)):
            subtemplates = load_template_files(
                os.path.join(template_dir, file),
                os.path.join(prefix, file));
            # Merge subtemplates into supertempaltes
            templates.update(subtemplates)
        else:
            # This is a template file. Add this 
            if prefix == "":
                key = file
            else:
                key = os.path.join(prefix, file)
               
            fd = open(os.path.join(template_dir, file), "r")
            templates[key] = fd.read()
            fd.close()
   
    return templates 

def generate_dpi_imports(tasks):
    ret = ""
    for task in tasks:
       print("task: " + task["name"]);
       
       if "type" in task.keys() and (task["type"] == "acc" or task["type"] == "req"):
           continue
       
       # Create DPI imports
       ret += "extern \"C\" uint32_t ${bfm}_" + task["name"] + "(uint32_t id";
       if "parameters" in task.keys():
           ret += ", "
           for param in task["parameters"]:
               ptr = " "
               
               if "dir" in param.keys() and param["dir"] == "output":
                   ptr = " *";
                     
               ptype = param["type"]
               ret += (ptype + ptr + param["name"] + ", ")
               
           ret = ret[:len(ret)-2]
            
       ret += ") {\n"
       ret += "  ${bfm}_t::bfm(id)->" + task["name"] + "("
       if "parameters" in task.keys():
           for param in task["parameters"]:
               ret += param["name"] + ", "
               
           ret = ret[:len(ret)-2]
       ret += ");\n"
       ret += "  return 0;\n";
       ret += "}\n"    

    return ret; 

def generate_dpi_export_method_decl(tasks):
    ret = ""
    for task in tasks:
       if task["type"] == "ack":
           continue
       
       # Declare the DPI-export API
       ret += "    void " + task["name"] + "(";
       if "parameters" in task.keys():
           for param in task["parameters"]:
               ptr = " "
               
               if "dir" in param.keys() and param["dir"] == "output":
                   ptr = " *";
                     
               ptype = param["type"]
               ret += (ptype + ptr + param["name"] + ", ")
               
           ret = ret[:len(ret)-2]
            
       ret += ");\n"

    return ret; 

def generate_dpi_export_method_def(tasks):
    ret = ""
    for task in tasks:
        if task["type"] == "ack":
            continue
       
        ret += "void ${bfm}_base::" + task["name"] + "(";
        if "parameters" in task.keys():
            for param in task["parameters"]:
                ptr = " "
               
                if "dir" in param.keys() and param["dir"] == "output":
                    ptr = " *";
                     
                ptype = param["type"]
                ret += (ptype + ptr + param["name"] + ", ")
               
            ret = ret[:len(ret)-2]
            
        ret += ") {\n"
        ret += "    GoogletestHdl::setContext(getContext());\n"
        ret += "    ${bfm}_" + task["name"] + "(";
        if "parameters" in task.keys():
            for param in task["parameters"]:
                ret += param["name"] + ", "
               
            ret = ret[:len(ret)-2]
        ret += ");\n"
        ret += "}\n"    

    return ret; 

def generate_dpi_export_func_decl(tasks):
    ret = ""
    for task in tasks:
        if task["type"] == "ack":
            continue
       
        ret += "extern \"C\" void ${bfm}_" + task["name"] + "(";
        if "parameters" in task.keys():
            for param in task["parameters"]:
                ptr = " "
               
                if "dir" in param.keys() and param["dir"] == "output":
                    ptr = " *";
                     
                ptype = param["type"]
                ret += (ptype + ptr + param["name"] + ", ")
               
            ret = ret[:len(ret)-2]
            
        ret += ");\n"

    return ret; 

def generate_rsp_if_api_decl(tasks):
    ret = ""
    for task in tasks:
        if task["type"] != "ack":
            continue
       
        ret += "    virtual void " + task["name"] + "(";
        if "parameters" in task.keys():
            for param in task["parameters"]:
                ptr = " "
               
                if "dir" in param.keys() and param["dir"] == "output":
                    ptr = " *";
                     
                ptype = param["type"]
                ret += (ptype + ptr + param["name"] + ", ")
               
            ret = ret[:len(ret)-2]
            
        ret += ") = 0;\n"

    return ret; 

def generate_sv_dpi_api(tasks):
    ret = ""
    for task in tasks:
        if task["type"] == "ack":
            # Declare a task for the BFM writer to call
            # 
            ret += "    task " + task["name"] + "("
            if "parameters" in task.keys():
                for param in task["parameters"]:
               
                    if "dir" in param.keys() and param["dir"] != "input":
                        print("Error: ack tasks cannot have output parameters")
                     
                    ptype = param["type"]
                    if ptype == "int8_t":
                        ptype = "byte"
                    elif ptype == "uint8_t":
                        ptype = "byte unsigned"
                    elif ptype == "int16_t":
                        ptype = "short"
                    elif ptype == "uint16_t":
                        ptype = "short unsigned"
                    elif ptype == "int32_t":
                        ptype = "int"
                    elif ptype == "uint32_t":
                        ptype = "int unsigned"
                    elif ptype == "int64_t":
                        ptype = "longint"
                    elif ptype == "uint64_t":
                        ptype = "longint unsigned"
                    elif ptype == "string":
                        ptype = "string"
                    else:
                        print("Error: unknown type \"" + ptype + "\"")
                    
                    ret += (ptype + " " + param["name"] + ", ")
               
                ret = ret[:len(ret)-2]
            
            ret += ");\n"
            ret += "        ${bfm}_" + task["name"] + "(m_id, "
            if "parameters" in task.keys():
                for param in task["parameters"]:
                    ret += param["name"] + ", "
            ret = ret[:len(ret)-2]
            ret += ");\n"            
            ret += "    endtask\n"
            # Define a DPI import for the BFM-writer task to call
            ret += "    import \"DPI-C\" context task ${bfm}_" + task["name"] + "(int unsigned id, "

            if "parameters" in task.keys():
                for param in task["parameters"]:
               
                    if "dir" in param.keys() and param["dir"] != "input":
                        print("Error: ack tasks cannot have output parameters")
                     
                    ptype = param["type"]
                    if ptype == "int8_t":
                        ptype = "byte"
                    elif ptype == "uint8_t":
                        ptype = "byte unsigned"
                    elif ptype == "int16_t":
                        ptype = "short"
                    elif ptype == "uint16_t":
                        ptype = "short unsigned"
                    elif ptype == "int32_t":
                        ptype = "int"
                    elif ptype == "uint32_t":
                        ptype = "int unsigned"
                    elif ptype == "int64_t":
                        ptype = "longint"
                    elif ptype == "uint64_t":
                        ptype = "longint unsigned"
                    elif ptype == "string":
                        ptype = "string"
                    else:
                        print("Error: unknown type \"" + ptype + "\"")
                    
                    ret += (ptype + " " + param["name"] + ", ")
               
            ret = ret[:len(ret)-2]
            
            ret += ");\n"
        elif task["type"] == "acc":
            ret += "export \"DPI-C\" function ${bfm}_" + task["name"] + ";\n"
        elif task["type"] == "req":
            # Export the task provided by the BFM writer
            ret += "    export \"DPI-C\" task ${bfm}_" + task["name"] + ";\n"
        else:
            print("Error: unknown task type \"" + task["type"] + "\"")
       
    return ret; 

#********************************************************************
#* generate_tasks()
#********************************************************************
def generate_tasks(template_vars, tasks):
   
#   template_vars["bfm_rsp_if_api"] = bfm_rsp_if_api
#   template_vars["bfm_sv_vif_api"] = bfm_sv_vif_api
#   template_vars["bfm_sv_dpi_api"] = bfm_sv_dpi_api
    template_vars["bfm_dpi_export_method_decl"] = generate_dpi_export_method_decl(tasks)
    template_vars["bfm_dpi_export_method_def"] = generate_dpi_export_method_def(tasks)
    template_vars["bfm_dpi_export_func_decl"] = generate_dpi_export_func_decl(tasks)
    template_vars["bfm_dpi_imports"] = generate_dpi_imports(tasks)
    template_vars["bfm_rsp_if_api"] = generate_rsp_if_api_decl(tasks)
    template_vars["bfm_sv_dpi_api"] = generate_sv_dpi_api(tasks)
   
    
#********************************************************************
#* gen_ifc()
#*
#* - gvm/<name>_base.cpp, <name>_base.h, <name>_rsp_if.h
#* - <name>_api_pkg.sv -- API to communicate BFM->UVM
#* - <name>_api.svh -- BFM API implementations
#********************************************************************
def gen_ifc(template_dir, args):
    print("gen_ifc: template_dir=" + template_dir)
    bfm_templates = load_template_files(
        os.path.join(template_dir, "bfm"), "")
    
    template_vars = {}
    name = os.path.splitext(os.path.basename(args.file))[0]
    template_vars["bfm"] = name
    
    # Load JSON
    bid_file = open(args.file, "r")
    bid_data = ""
    for line in bid_file.readlines():
        ci = line.find("#")
        if ci != -1:
            line = line[:ci] + "\n"
        bid_data += line

    bid = json.loads(bid_data)
    bid_file.close()
    
    if "tasks" in bid.keys():
        generate_tasks(template_vars, bid["tasks"])
    else:
        print("Error: no 'tasks' section")

    # Re-substitute to expand recursive variable refs
    for key in template_vars.keys():
        template_var_t = Template(template_vars[key])
        template_vars[key] = template_var_t.safe_substitute(template_vars)

    print("o=" + args.o)
    outdir = args.o
    
    # First check to see if there are any output-path conflicts
    if args.force != True:
        for key in bfm_templates.keys():
            if key.startswith("bfm_"):
                out_file = name + key[3:]
            else:
                out_file = key
            
            out_path = os.path.join(outdir, out_file)
        
            if os.path.exists(out_path):
                print("Error: output path \"" + out_path + "\" already exists")
                exit(1)
    
    for key in bfm_templates.keys():
        leaf = os.path.basename(key)
        
        if leaf.startswith("bfm_"):
            out_file = os.path.join(os.path.dirname(key), name + leaf[3:])
        else:
            out_file = key
            
        out_path = os.path.join(outdir, out_file)
        
        if os.path.isdir(os.path.dirname(out_path)) == False:
            os.makedirs(os.path.dirname(out_path))

        out_fd = open(out_path, "w")
        template = Template(bfm_templates[key])
        
        print("Note: creating file " + out_path)
        
        out_fd.write(template.safe_substitute(template_vars))
        out_fd.close()
        
#********************************************************************
#* main()
#********************************************************************
def main():
    
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="subcmd")
    
    gen_bfm = subparser.add_parser("gen-ifc")
    gen_bfm.add_argument("-o", help="output directory", default=".")
    gen_bfm.add_argument("-force", action="store_true", help="force overwriting output")
    gen_bfm.add_argument("file", help="BFM Interface definition")
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    print("script_dir: " + script_dir);
    src_dir = os.path.dirname(script_dir)
    print("src_dir: " + src_dir);
    template_dir = os.path.join(os.path.dirname(src_dir), "templates")
    print("template_dir: " + template_dir);
    
    args = parser.parse_args()

    if args.subcmd == "gen-ifc":
        gen_ifc(template_dir, args)
    else:
        print("Error: unknown sub-command")
       

if __name__ == "__main__":
    main()
    