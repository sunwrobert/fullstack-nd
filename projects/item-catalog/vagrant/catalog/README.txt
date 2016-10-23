# Item Catalog: Music Lovers

### About

This application displays a list of items (Artists) within a variety of categories (genres) and also includes Authentication and Authorization using Google Sign in. Registered users will have the ability to post, edit and delete their own items.

### How to run

1. Download or clone the `fullstack-nd/projects/item-catalog` directory.
2. Initialize the Vagrant vm via `vagrant up`, which should set up on `localhost:5000`.
3. Connect to the virtual machine: `vagrant ssh`.
4. Navigate to the catalog directory: `cd /vagrant/catalog`
5. Start the server: `python app.py`.
6. Navigate to `localhost:5000`

NOTE: You need to make your own database solution for running this locally, as the app currently uses a public heroku postgres database.