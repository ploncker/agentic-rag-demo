# agentic RAG demo

Building up on [this excellent video from AI Makerspace](https://www.youtube.com/watch?v=SEA3eJrDc-k), this project implements a RAG system that queries data about... RAG systems.

It uses a Streamlit UI to interact with the RAG system. The app is accessible on https://rag.yactouat.com.

The LLMs under the hood are a mixture of ChatGPT 4 and 3.5.

## pre requisites

To be able to use the application, you need:

- a working Python environment (I use 3.12)
- an OpenAI API key

For the OpenAI API key, if it's not loaded from a `.env` file, the user will be prompted to enter it.

## run locally

To run the application locally: `streamlit run streamlit_app.py` OR `python3 -m streamlit run streamlit_app.py`.

## run on an Ubuntu server

Deployment is done using GitHub Actions, you need to fill in a few repository secrets, as stated in the `.github/workflows/cicd.yml` file.

Before you push to the master branch and deploy the app, make sure you have followed these steps:

- `mkdir ~/agentic-rag-demo`
- `sudo apt update && sudo apt upgrade -y`
- `sudo apt install nginx`
- configure an A record in your DNS settings to point to your server's IP address for your domain or subdomain
- `sudo mkdir -p /var/www/<domain>` (replace `<domain>` with your domain or subdomain)
- `sudo chown -R www-data:www-data /var/www/<domain>`
- `sudo chmod -R 755 /var/www/<domain>`
- `sudo touch /var/www/<domain>/index.html` and add some dummy content in it
- `sudo nano /etc/nginx/sites-available/<domain>.conf`
- add the following content:

```
server {
    listen 80;
    listen [::]:80;

    root /var/www/<domain>;
    index index.html;

    server_name <domain>;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

- `sudo ln -s /etc/nginx/sites-available/<domain>.conf /etc/nginx/sites-enabled/`
- `sudo nginx -t`
- `sudo systemctl reload nginx`
- at this point, you should be able to see the dummy content when you navigate to your domain or subdomain on plain HTTP
- after having deployed the code, run `nohup streamlit run streamlit_app.py --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=true &>/dev/null &` on the server to launch the app in the background (the CI stops the current app)
- you can now update your Nginx conf like so, to serve the app:

```
server {
    listen 80;
    listen [::]:80;

    root /var/www/<domain>;
    index index.html;

    server_name <domain>;

    location / {
        proxy_pass http://0.0.0.0:8501;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

}
```

- `sudo nginx -t`
- `sudo systemctl reload nginx`
- you should now be able to see the app on your domain or subdomain on plain HTTP
- now follow the instructions on certbot website to put the app behind HTTPS
