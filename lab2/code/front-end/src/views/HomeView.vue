<template>
  <div class="common-layout main-page">
    <el-container>
      <el-header>
        <div class="head-font">
          Image Search System
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu default-active="1" class="el-menu-vertical-demo" @select="handleSelect">
            <el-menu-item index="1">
              <el-icon>
                <Search />
              </el-icon>
              <span>图片搜索</span>
            </el-menu-item>
            <el-menu-item index="2">
              <el-icon>
                <Star />
              </el-icon>
              <span>我的收藏</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <div v-if="showMode == 1">
            <el-card class="box-card">
              <div class="upload-tips">请上传jpg/png文件，并且图片大小不建议超过500kb</div>
              <el-upload class="upload-demo" action="http://127.0.0.1:5000/imgUpload" :on-success="handleSuccess"
                :on-preview="handlePreview" :on-remove="handleRemove" v-model:file-list="fileList" list-type="picture">
                <div><el-button size="small" type="primary">点击上传图片 </el-button></div>
              </el-upload>

              <div>
                <el-select v-model="value" class="m-2" placeholder="Select">
                  <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
                <el-button type="success" @click="startFilter">搜索</el-button>
              </div>
            </el-card>
            <h4>共搜索到 <span>{{ showList.length }}</span> 张图片</h4>
            <el-row :gutter="60">
              <el-col :span="8" v-for="item in showList" :key="item">
                <el-card :body-style="{ padding: '2px' }" class="img-card">
                  <el-row :gutter="20">
                    <el-col :span="15" :offset="1">
                      <el-row><el-image class="show-img" :src="item.imgUrl" /></el-row>
                      <el-row class="img-tag">
                        <el-col :span="8" v-for="tag in item.imgTag" :key="tag">
                          <el-tag class="ml-2" type="success" size="small" style="margin-top: 5px;">{{ tag }}</el-tag>
                        </el-col>
                      </el-row>
                    </el-col>
                    <el-col :span="3" :offset="1">
                      <el-row class="img-description">
                        {{ item.imgName }}
                      </el-row>
                      <el-row style="margin-left: 30%;margin-top:150px;">
                        <el-button type="warning" @click="addMyFavorites(item)" circle>
                          <el-icon>
                            <Star />
                          </el-icon>
                        </el-button>
                      </el-row>

                    </el-col>
                  </el-row>


                </el-card>
              </el-col>
            </el-row>
          </div>
          <div v-if="showMode == 2">
            <h4>共收藏有 <span>{{ favorites.length }}</span> 张图片</h4>
            <el-row :gutter="60">
              <el-col :span="8" v-for="item in favorites" :key="item">
                <el-card :body-style="{ padding: '2px' }">
                  <el-image class="show-img" :src="item" />
                  <div style="padding: 2px;">
                    <span>图片名称：{{ item.slice(item.indexOf("im")) }}</span>
                    <div class="bottom clearfix">
                      <el-button type="danger" @click="deleteMyFavorites(item)" circle>
                        <el-icon>
                          <Delete />
                        </el-icon>
                      </el-button>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
/* eslint-disable */
import { reactive, ref } from 'vue';
import { ElMessage } from 'element-plus';
import axios from "axios";
export default {
  name: 'HomeView',
  setup() {
    let showMode = ref(1);//控制展示的是搜索界面(1)还是收藏界面(2)

    /**
     * @description: 上传图片
     */
    let imgList = reactive([]);//接收到的图片列表
    let fileList = reactive([]);//上传的图片
    const handleRemove = (uploadFile, uploadFiles) => {
      console.log(uploadFile, uploadFiles)
    }

    const handlePreview = (file) => {
      console.log(file)
    }

    const handleSuccess = (response, file) => {
      imgList.length = 0;

      for (let i = 0; i < response.image_list.length; i++) {
        var imgName = (response.image_list[i]).replace("\\", "/")
        var imgUrl = "http://127.0.0.1:5000" + imgName;
        var imgTag = response.tag_list[i];
        imgName = imgName.slice(imgName.indexOf('im'))
        var imgValue = {
          imgUrl,
          imgTag,
          imgName
        }
        imgList.push(imgValue)
      }

      //console.log('接收到的图片',imgList);
      showMode.value = 1;
    }

    /**
     * @description: 控制搜索与条件筛选
     */

    let showList = reactive([]);

    const value = ref('any')

    const options = [
      {
        value: 'any',
        label: 'any',
      },
      {
        value: 'animals',
        label: 'animals',
      },
      {
        value: 'baby',
        label: 'baby',
      },
      {
        value: 'bird',
        label: 'bird',
      },
      {
        value: 'car',
        label: 'car',
      },
      {
        value: 'clouds',
        label: 'clouds',
      },
      {
        value: 'dog',
        label: 'dog',
      },
      {
        value: 'female',
        label: 'female',
      },
      {
        value: 'flower',
        label: 'flower',
      },
      {
        value: 'food',
        label: 'food',
      },
      {
        value: 'indoor',
        label: 'indoor',
      },
      {
        value: 'lake',
        label: 'lake',
      },
      {
        value: 'male',
        label: 'male',
      },
      {
        value: 'night',
        label: 'night',
      },
      {
        value: 'people',
        label: 'people',
      },
      {
        value: 'plant_life',
        label: 'plant_life',
      },
      {
        value: 'portrait',
        label: 'portrait',
      },
      {
        value: 'portrait',
        label: 'portrait',
      },
      {
        value: 'river',
        label: 'river',
      },
      {
        value: 'sea',
        label: 'sea',
      },
      {
        value: 'structures',
        label: 'structures',
      },
      {
        value: 'sunset',
        label: 'sunset',
      },
      {
        value: 'transport',
        label: 'transport',
      },
      {
        value: 'tree',
        label: 'tree',
      },
      {
        value: 'water',
        label: 'water',
      },
    ]

    const startFilter = () => {
      showList.length = 0;


      for (let i in imgList) {
        // console.log(imgList[i])
        // console.log(imgList[i].imgTag)
        // console.log(value.value)
        if (value.value == 'any') {
          showList.push(imgList[i])
        }
        else {
          var tagSet = imgList[i].imgTag
          for (let j in tagSet)
            if (tagSet[j] == value.value) {
              showList.push(imgList[i])
            }
        }
      }
      console.log('展示的内容', showList)
    }

    /**
     * @description: 处理收藏逻辑
     */

    let favorites = reactive([]);

    const addMyFavorites = (item) => {
      var imgId = item.imgName.slice(item.imgName.indexOf("im") + 2)
      imgId = imgId.substring(0, imgId.indexOf('.'))
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/star",
        params: {
          'id': imgId
        }
      }).then(function (response) {
        successMsg()
      })
    }

    const deleteMyFavorites = (item) => {
      console.log(item)
      var imgId = item.slice(item.indexOf("im") + 2)
      imgId = imgId.substring(0, imgId.indexOf('.'))
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/star",
        params: {
          'id': imgId
        }
      }).then(function (response) {
        successMsg()
        window.location.reload()
      })
    }
    const showMyFavorites = () => {
      favorites.length = 0;
      axios({
        method: "get",
        url: "http://127.0.0.1:5000/star/all",
      }).then(function (response) {
        console.log()
        for (let i in response.data) {
          var imgId = response.data[i]
          var url = "http://127.0.0.1:5000/favorite/im" + imgId + ".jpg"
          console.log(url)
          favorites.push(url)
        }
      })
      //console.log(favorites);
    }


    /**
     * @description: 处理菜单切换
     */
    const handleSelect = (index) => {
      //console.log('index', index)
      showMode.value = index;
      if (showMode.value == 2) {
        console.log('查看收藏')
        showMyFavorites();
      }

    }

    const successMsg = () => {
      ElMessage({
        message: '成功修改收藏状态！',
        type: 'success',
      })
    }


    return {
      showMode,
      fileList,
      imgList,
      favorites,
      handleRemove,
      handlePreview,
      handleSuccess,
      addMyFavorites,
      showMyFavorites,
      handleSelect,
      successMsg,
      deleteMyFavorites,
      showList,
      value,
      options,
      startFilter
    }
  }
}


</script>

<style>
.el-header {
  background-color: #143761;
  color: #f1ecec;
  height: 10vh;
}

.head-font {
  margin-top: 1vh;
  color: gold;
  font-size: 2vh;
  text-align: center;
}

.layout-container-demo .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}

.layout-container-demo .el-menu {
  border-right: none;
}

.box-card {
  margin-bottom: 2vh;
  background-color: azure;
}

.img-card {
  width: 360px;
  height: 300px;
  margin-top: 10px;
}

.main-page {
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
}

.show-img {
  width: 260px;
  height: 200px;
  margin-top: 5px;
}

.upload-tips {
  margin-bottom: 15px;
}

.img-description {
  font-weight: 600;
  margin-top: 30px;
  text-align: center;
}

.img-tag {
  margin-top: 15px;
}
</style>
