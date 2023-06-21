import json

tag_type = ['animals', 'baby', 'bird', 'car', 'clouds', 'dog', 'female',
            'flower', 'food', 'indoor', 'lake', 'male', 'night', 'people',
            'plant_life', 'portrait', 'river', 'sea', 'structures', 'sunset',
            'transport', 'tree', 'water']


def image_tags():
    imgDict = dict()
    for i in tag_type:

        # 读取对应的文件
        with open('database/tags/' + i + '.txt', 'r') as fp:
            li = fp.readlines()
            for j in li:
                img_name = "im" + j.strip() + ".jpg"
                if img_name in imgDict.keys():
                    imgDict[img_name].append(i)
                else:
                    imgDict[img_name] = []
                    imgDict[img_name].append(i)
    print(imgDict['im45.jpg'])

    with open('img_tag.json', 'w') as f:
        json.dump(imgDict, f)


image_tags()
