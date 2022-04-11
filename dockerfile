FROM ubuntu

RUN apt-get update
RUN apt-get install -y nginx

RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential python3-gunicorn
RUN apt-get install -y git
RUN mkdir /var/www && cd /var/www
RUN git clone https://github.com/MrCooki/Responsive.git
RUN chown -R www-data:www-data /var/www/Responsive


RUN pip3 install pipenv
RUN pipenv install

RUN gunicorn --workers 5 wsgi:app

RUN cp responsive.conf /etc/nginx/sites-available/responsive.conf
RUN ln -s /etc/nginx/sites-available/responsive.conf /etc/nginx/sites-enabled/
RUN systemctl restart nginx

RUN cp responsive.service /etc/systemd/system/responsive.service
RUN systemctl restart responsive.service 
RUN systemctl daemon-reload 



