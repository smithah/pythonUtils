# coding: utf8
import json
import PIL.FontFile
import PIL.ImageFont
import fitz
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import configparser
import pymupdf
import PIL

config = configparser.ConfigParser()
config.read('fontconfigfile.ini')
filename = config["file.paths"]["IN_FILEPATH"]
fontcode = config['fonts.example']['FONTCODE']
font = fitz.Font(fontcode)
doc = fitz.open(filename)
doc.subset_fonts()
UNDERNEATH = False 
WIDTH = 0
HEIGHT = 0 

def getOptimalFontSize(font_size, rect,text_string):
        text = text_string
        fontsize = font_size
        #size = None
        
       
        while font_size > 1:
            if sum(font.char_lengths(text_string+" ",fontsize=fontsize)) < rect.width:
                break
            fontsize -= 1          

        return fontsize

def iterate_nested_json_for_loophw(json_obj,WIDTH,HEIGHT):
    for key, value in json_obj.items():
        if isinstance(value, dict):
            iterate_nested_json_for_loophw(value,WIDTH,HEIGHT)
        else:
            if(key == "width"):
                WIDTH = float(value)
                print(WIDTH)
            if(key == "height"):
                HEIGHT = float(value)
                print(HEIGHT)
    return WIDTH,HEIGHT

# Add a page and insert text 
def itrdic(dicti):
    index = 0   
    for j in dicti:
        page = doc[index]
        shape = page.new_shape()
        xref = page.xref  # the page's object number
        fontcode = config['fonts.example']['FONTCODE']
        fontfamily = config['fonts.example']['FONTFAMILY']
        fontfile = config['fonts.example']['NOTOSANSDEVANAGARI']
        font = fitz.Font(fontcode)
        
        s = doc.xref_object(xref)  # get the definition string 
        s = s.replace(str(WIDTH), str(HEIGHT))  # double the page height
        doc.update_object(xref, s)  # write back the changed page definition
        
        for key1, value1 in j.items():                    
                    if(key1 == "texts"):                    
                        for data in value1:                                                             
                                top = float(data["top"])
                                left = float(data["left"])
                                end_left = float(data["end_left"])
                                end_top = float(data["end_top"])
                                if(len(data['text'][0]["fontWeight"]) != 0):
                                    x = data['text'][0]["fontWeight"].split()
                                    cssFontdec = ""
                                    for ind in range(len(x)):                                    
                                        val = x[ind]                                         
                                        match val:                                        
                                            case "underline":
                                                cssFontdec = cssFontdec + "text-decoration: "+x[ind]+";"
                                                text_decoration = x[ind]
                                                break
                                            case "superscript":
                                                cssFontdec = cssFontdec + "vertical-align: super ;"
                                                break
                                            case "bold":
                                                cssFontdec =cssFontdec + "font-weight: "+x[ind]+";"
                                                break
                                        
    
                                if(len(data['text'][0]["colorCode"]) != 0):  # WARNING:
                                    h = data['text'][0]["colorCode"].lstrip('#')                         
                                    
                                original_text = data['text'][0]["text"]
                                if(len(data['text'][0]["text"]) != 0) and top.is_integer and left.is_integer:
                                    
                                    reshaped_text = reshape(original_text)
                                    bidi_text = get_display(reshaped_text)
                                    x0 = left
                                    y0 = top   
                                    x1 = end_left
                                    y1 = end_top
                                    
                                                          
                                    if(len(data['text'][0]["font_size"]) != 0):
                                        
                                       
                                        font_size = float(str(data['text'][0]["font_size"]))                                        
                                        rect = pymupdf.Rect(x0, y0, x1,y1)
                                        print(rect)
                                        font_size = getOptimalFontSize(font_size,rect,bidi_text)                                                                           
                                        page.wrap_contents()                                     
                                        arch=pymupdf.Archive()
                                        
                                        css=pymupdf.css_for_pymupdf_font(fontcode, archive=arch, name=font.name)
                                        css += "* {font-family:'"+fontfamily+"','DejaVu Sans','FiraGO Regular';}"
                                        print(css)
                                        cssStr = "body {font-size:"+str(font_size)+"pt;color:"+data['text'][0]["colorCode"]+";"+cssFontdec+";}"+css
                                    if(len(data['text'][0]["text"]) != 0) and (len(data['text'][0]["font_size"]) != 0):
                                            
                                            page.clean_contents(sanitize=True)
                                            
                                            page.insert_htmlbox(  # page is a PDF Page object
                                                rect,         # rectangle inside the page
                                                bidi_text,         # text string or a Story object
                                                css=cssStr,                                               
                                                scale_low=0,  # limit scaling down when fitting content
                                                archive=arch, # points to locations of fonts and images
                                                rotate=0,     # clockwise rotate content by this angle
                                                oc=0,         # assign xref of an OCG (conditional visibility)
                                                opacity=1,    # make content transparent (default: 1 = no)
                                                overlay=True
                                                 # put in foreground (default) or background
                                            )                                            
                                            
                                            page.clean_contents(sanitize=True)
                                   
                                    
        index = index + 1

thislist= []     

with open(config["file.paths"]["JSON_FILE"],encoding="utf8") as f:
    d = json.load(f)
    for i in d:        
            WIDTH, HEIGHT = iterate_nested_json_for_loophw(i,WIDTH,HEIGHT)      
            for key, value in i.items():                
                if isinstance(value, dict):                   
                    thislist.append(value)          
    itrdic(thislist) 


doc.subset_fonts()
doc.ez_save(config["file.paths"]["OUT_FILEPATH"],garbage=3, deflate=True)                 
doc.close()    
    




