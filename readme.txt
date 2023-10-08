Django REST Framework Image Upload API

Description
This is a simple API built using Django and Django REST Framework that allows users to upload images.
The API supports different account tiers with varying features, such as thumbnail generation and expiring links to images.

The whole project is Dockerized so you can build a container and whole project should automatically install all required dependencies.

You can POST new images like that 
```
POST /upload_image/
```
or get your current images
```
GET /list_images/
```

Currently the project supports three build-in groups that have abilities to create 200x200 thumbnails (Basic), 400x400 and same as Basic (Enterprise), and link to original image, expiring image (specified after 300-3000 sec),
that deleted itself from DB after this time (Enterprise)
It's easy to introduce new groups just by modeling serializers and views.
