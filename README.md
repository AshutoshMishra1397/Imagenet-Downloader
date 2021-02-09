# Imagenet-Downloader
Python program to download images from www.image-net.org

sample commands that you can try:
(make sure you are in same directory in terminal as the .py and .json files for these commands to run)

1) 
Download 20 images of Persian cats:
python Imagenet_Downloader.py --subclass_list "Persian cat" --main_class "cat" --data_root "./" --imagenet_info_json "./imagenet_class_info.json" --images_per_subclass 20

2) 
Download 20 images of hunting dog and shepherd dog each:
python Imagenet_Downloader.py --subclass_list "hunting dog" "shepherd dog" --main_class "dog" --data_root "./" --imagenet_info_json "./imagenet_class_info.json" --images_per_subclass 20


