# Image Search System

This project is a simple image search system, with the front-end using Vue.js and the back-end using the Flask framework. The following are explanations of each part.

## Front End

The front-end mainly uses Vue3 and Element Plus to implement the interface, and Axios is used to complete the connection with the backend. To start the front-end, you can use the following command

##### Project setup

```
npm install
```

##### Compiles and hot-reloads for development
```
npm run serve
```

After completing the above operations and starting the backend service locally, you can directly access the http://localhost:8080/ Accessing pages.

## Back End

The backend is based on the Flask framework and implements a deep learning based image similarity search using TensorFlow and some publicly available datasets.

### How to run

1. Download [imagenet](https://drive.google.com/open?id=1UOyZ8166qM3SzxGvaUeWpBzSUfoQLUjJ) folder, extraxt and keep it in server directory
2. Download the existing project framework, and add a favorites.txt in the database folder. Then you should copy all files in the code/server folder of the submitted compressed package to the server folder of the project. The following is the project file architecture.

```
      root folder  
      │
      └───__init__.py
      │   
      └───server
      |   │───database
      |        │────dataset
      |        │────tags
      |        │────favorites.txt
      |   │───imagenet
      |   │───static
      |   │───templates
      |   │───uploads
      |   │───rest-server.py
      |   │───search.py
      |   │───image_vectorizer.py
      |   │───process_tag.py
```

3. Run image vectorizer which passes each data through an inception-v3 model and collects the bottleneck layer vectors and stores in disc. Edit dataset paths accordingly indide the image_vectorizer.py

```
  python server/image_vectorizer.py 
```

   This will generate two files namely, image_list.pickle and saved_features.txt. Keep them inside lib folder where search.py script is available.

4. Run process_tag.py which can generate a JSON file that stores the mapping relationship between images and tags based on the image tag information in the database.

   ```
     python server/process_tag.py 
   ```

   Afterwards, you can check and see a file named img_tag.json in the server folder.

5. Start the server by running rest-server.py. This project uses flask based REST implementation for UI.

```
  python server/rest-server.py 
```

## How to Use

After both the current and backend are started, access the url  http://localhost:8080/ to get the UI. 

The initial page is as follows:

![image-20230505093107854](https://s2.loli.net/2023/05/05/7szYhD9xcPuTF8Z.png)

### Search function

1. Click the upload button and select the image you want to search for.（Suggest using example_ The images in the photo folder are used to view the demonstration, and the results will be better）

   ![image-20230505093433058](https://s2.loli.net/2023/05/05/ypnTxDF8tr3JbW7.png)

2. The default filter criterion is any, click the search button.

   ![image-20230505152329355](https://s2.loli.net/2023/05/05/AZmfDedbnyV4xXM.png)

3. You can also modify the filtering parameters and select the desired tag for search.

   ![image-20230505152402321](https://s2.loli.net/2023/05/05/k8t2yLXewZE6iF1.png)

### Collection function

1. Click on the 'Favorite' button in the search results, taking 'Favorite im1475.jpg' as an example here.

   ![image-20230505152430869](https://s2.loli.net/2023/05/05/zojLahyCVmilrW3.png)

2. Click on "My Favorites" in the menu on the left column to view the collection results.

   ![image-20230505152450729](https://s2.loli.net/2023/05/05/aIZ8otrmFM7X63G.png)

3. To cancel the collection, click the red button to delete it.