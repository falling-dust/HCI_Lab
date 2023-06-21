#!flask/bin/python
################################################################################################################################
# ------------------------------------------------------------------------------------------------------------------------------
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
# -------------------------------------------------------------------------------------------------------------------------------
################################################################################################################################
import json
import re
import shutil
from glob import glob
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect, render_template, Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil
import numpy as np
from search import recommend
from flask_cors import CORS
import tarfile
from datetime import datetime
from scipy import ndimage

# from scipy.misc import imsave

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile

app = Flask(__name__, static_url_path="")
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

# ==============================================================================================================================
#
#    Loading the extracted feature vectors for image retrieval
#
#
# ==============================================================================================================================
extracted_features = np.zeros((2955, 2048), dtype=np.float32)
with open('saved_features_recom.txt') as f:
    for i, line in enumerate(f):
        extracted_features[i, :] = line.split()
print("loaded extracted_features")


# ==============================================================================================================================
#
#  This function is used to do the image search/image retrieval
#
# ==============================================================================================================================
@app.route('/imgUpload', methods=['GET', 'POST'])
# def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_img():
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):
        os.mkdir(result)
    shutil.rmtree(result)

    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:  # and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/result"
            image_list = [os.path.join(image_path, file) for file in os.listdir(result)
                          if not file.startswith('.')]

            # 将图片的tag返回给前端
            tag_list = []
            with open('img_tag.json', 'r') as f:
                img_tag = json.load(f)
                for image in image_list:
                    image_id = re.search('.*?(\d+).jpg', image).group(1)
                    try:
                        tag_list.append(img_tag[f'im{image_id}.jpg'])
                    except:
                        tag_list.append('none')
            images = {
                'image_list': image_list,
                'tag_list': tag_list,
            }
        return jsonify(images)


# 获取用户全部收藏，返回的是图片的id
@app.route('/star/all', methods=['GET'])
def get_all_star():
    res = []
    with open('database/favorites.txt', mode='r') as f:
        for i in f.readlines():
            res.append(i.strip())
    return jsonify(res)


# 改变图片收藏状态
@app.route('/star', methods=['POST'])
def change_img_star():
    imageId = request.values.get('id')
    # print(imageId)
    # 获取收藏夹的内容
    with open('database/favorites.txt', mode='r') as f:
        s = f.readlines()

    p = []
    # 判断收藏是否已经存在
    isCollected = False
    for i in s:
        if i.strip() == imageId:
            isCollected = True
        else:
            p.append(i.strip())

    # 如果没有收藏，则将其添加到静态资源中
    if not isCollected:
        p.append(imageId)
        mycopyfile('./database/dataset/im' + imageId + '.jpg', './static/favorite/')
    else:
        os.remove('./static/favorite/im' + imageId + '.jpg')  # 若收藏了，则将其移除
    # 写文件
    n = len(p)
    with open('database/favorites.txt', mode='w') as f:
        for index, item in enumerate(p):
            if index != n - 1:
                f.write(item + '\n')
            else:
                f.write(item)

    return jsonify({
        'status': True,
    })


# 复制函数
def mycopyfile(srcfile, dstpath):  # 复制函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.copy(srcfile, dstpath + fname)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstpath + fname))


# ==============================================================================================================================
#
#                                           Main function                                                        	            #
#
# ==============================================================================================================================
@app.route("/")
def main():
    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
