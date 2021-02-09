# -*- coding: utf-8 -*-

"""
Created on Thu Feb  4 21:23:14 2021

@author: Ashutosh Mishra
"""
import torchvision,torch, torch.utils.data, glob,os, numpy, PIL, argparse, requests,logging, json
from PIL import Image
from requests.exceptions import ConnectionError,ReadTimeout,TooManyRedirects,MissingSchema,InvalidURL

parser = argparse.ArgumentParser(description ='HW02 Task1')
parser.add_argument('--subclass_list',nargs ='*',type =str,required = True)
parser.add_argument('--images_per_subclass', type =int,required = True)
parser.add_argument('--data_root', type =str , required =True )
parser.add_argument('--main_class',type =str , required =True )
parser.add_argument('--imagenet_info_json',type =str,required = True )
args, args_other = parser.parse_known_args()



#Reference for get_image method:https://github.com/johancc/ImageNetDownloader3
def get_image(img_url,class_folder):
    if len(img_url) <= 1:
        return 0
    try:
        img_resp = requests.get(img_url,timeout = 1)
    except ConnectionError:
        print('Connection Error')
        return 0
    except ReadTimeout:
        print("Read Time Out")
        return 0
    except TooManyRedirects :
        print("Too Many Redirects")
        return 0
    except MissingSchema:
        print("Missing Schema")
        return 0
    except InvalidURL:
        print("Invalid URL")
        return 0

    if not 'content-type' in img_resp.headers:
        print("Content type error")
        return 0
    if not 'image' in img_resp.headers['content-type']:
        print("Image type error")
        return 0
    if (len(img_resp.content)< 1000):
        return 0
    
    img_name = img_url.split('/')[-1]
    img_name = img_name.split("?")[0]
    
    if (len(img_name)<=1):
        print('Name Error')
        return 0
    if not 'flickr' in img_url:
        print("Flicker Error")
        return 0
    
    try:
        img_file_path = os.path.join(class_folder,img_name)
        with open(img_file_path,'wb') as img_f:
            img_f.write(img_resp.content)
        
            # Resize image to 64x64
        im = Image.open(img_file_path)
        if im.mode != "RGB":
            im = im.convert(mode="RGB ")
        im.save(img_file_path)
        return 1
             
    except:
        print("File Error")
        return 0

#Returns dictionary in the form ('class_name':'fileID')
def create_dict(path):          #path = path to the imagenet json file
    with open(path) as file:
        data = json.load(file)
    key = list(data.keys())
    val = list(data.values())
    arr = [];
    db  = dict()
    for i in range(len(key)):
        arr.append(val[i]['class_name'])
        db[arr[i]] = key[i]
    return db

#Returns the list of URLs based on subclass_list 
def get_url(database,subclass_list):
    base_url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid='
    url_list = []
    for i in range(len(subclass_list)):
        url_list.append(base_url+database[subclass_list[i]])
    return url_list
    

###########################################################

if(args.data_root[-1]=='/'):
    class_folder =  args.data_root+args.main_class
else:
    class_folder = args.data_root+'/'+args.main_class

try:
    os.makedirs(class_folder,exist_ok=True)
except OSError:
    pass

database = create_dict(args.imagenet_info_json)
urls = get_url(database,args.subclass_list)
id = []
for i in urls:
    resp = requests.get(i)
    id.append([url.decode('utf -8') for url in resp.content.splitlines()])

for i in range(len(args.subclass_list)):
    count = 0
    for j in range(len(id[i])):
        get_image(id[i][j], class_folder)
        count = len([name for name in os.listdir(class_folder)])-i*args.images_per_subclass
        print('Downloading...\t'+args.subclass_list[i]+'....'+str(count))
        if(count == args.images_per_subclass):
            break
    
                    