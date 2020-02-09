## Een HowTo voor de blog

Met de volgende post, probeer ik duidelijk te maken hoe je mits het gebruik van [mijn code](https://github.com/VincentBockaert/2019-2020-Stage-Blog), deze site zelf online kan brengen, of op zen minst lokaal kan testen.

De post is eerder in het formaat van een "guide/documentatie" en niet zo zeer een typische blog post, omdat ik niet persoonlijk niet goed als blog zou kunnen schrijven.

### Development setups

Je kan deze setup zowel op een Windows OS doen als op een Unix toestel. Hieronder leg ik alvast uit hoe je het voor zowel Windows 10 en Ubuntu kan doen.

---
***Environment variables***

De python code verwacht enkele environment variables, hierop wordt myBlog/myBlog/settings.py gecontroleerd.
Indien de environment variable "DEBUG" niet gezet werd, runned Django in productie-modus. Je zet dit dus best via `export DEBUG=1` (linux) of `SET DEBUG=1` (Windows), indien je in development-modus wil runnen.

Daarnaast zijn er nog meer _Environment Variables_ zoals MYSQL_PORT, die kan je gewoon negeren, als die niet gezet zijn is de code zodanig geschreven dat het automatisch sqlite3 gebruikt.

---

#### Linux Dev Setup

Je mileage kan variëren naargelang je reeds sommige van de packages geïnstalleerd hebt.

    sudo apt update
    sudo apt install python3-venv python3-dev python3-wheel python3-pip gcc
    sudo apt install libmysqlclient-dev # otherwise pip install -r requirements.txt will fail due to missing mysql_config file
    cd '2019-2020-Stage-Blog'
    source dev.env # set the dev environment variables DEBUG and SECRET_KEY
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    cd myBlog
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser
    python3 manage.py runserver
    # go to localhost:8000/admin to create your first blog post

#### Windows Dev Setup


---
***Note***

Het merendeel van de manuele testing dat ik doe, gebeurt op mijn Ubuntu laptop, het kan gebeuren dat dit ervoor zorgt dat de Dev Setup faalt op Windows door een dependency, zoals pip dat verwacht dat er enkele C/C++ libraries aanwezig zijn.
Python is en blijft vooral gericht op de Linux wereld, dus niet onmiddellijk concluderen dat alles fout is, waarschijnlijk mis je een library die Ubuntu by default al had, waardoor ik dit nooit had opgemerkt.

---

##### Requirements
* Python geïnstalleerd hebben
* Eventueel Visual Studio Build Tools
    * zodat pip goed kan functioneren wanneer het libraries verwacht 
    * daarom raad ik aan Python te installeren via de Visual Studio Installer

##### Commandos - Windows CMD

    # sets DEBUG=True
    ./env_setup.bat 
    python -m venv venv
    venv\Script\activate # you mind need to set --ExecutionPolicy ByPass if using Powershell instead of cmd
    python -m pip install -r requirements.txt
    cd myBlog
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    # go to localhost:8000/admin to create your first blog post

### Een blog post maken

Eenmaal je de dev setup gedaan hebt kan het handig zijn om ook effectief een blog post te maken, al was het maar om toch iets te zijn op de nu wel lege startpagina. 
Dit kan je makkelijk doen met behulp van de admin account, aangemaakt door `python3 manage.py createsuperuser`.
Surf naar localhost:8000/admin en de rest spreekt voor zich.

### RSS Feed

Django bied een high-level framework waarmee je met gemak een RSS feed kan opzetten.
Om je te subscriben op de feed, kan je de URL https://blog.vincentbockaert.xyz/feed of http://localhost:8000/feed toevoegen aan je RSS Feed Reader. 

Alternatief kan je simpelweg op de homepage laten zoeken naar een RSS Feed, een RSS Feed Reader Addon/Extensie zoals [Feedbro](https://addons.mozilla.org/en-US/firefox/addon/feedbroreader/) kan voor jou automatisch de feed toevoegen.
Uiteraard kan je zelf een titel toevoegen voor de RSS Feed.

### In Productie

Het is goed wel om het lokaal te kunnen testen en aan te passen, maar wat als je het zelf wil publiceren?
Heb geen vrees, met de magie genaamd **_containers_** van Docker kan je dit opzetten in no time.

Enige kennis van Linux distro's is vereist.

#### Environment variables

Om de applicaties in een productie omgeving te laten draaien moeten enkele omgevingsvariabelen ingesteld worden.
De Docker containers nemen via `--env-file` een bestand op en zet de omgevingsvariabelen daarin gedefiniëerd als omgevingsvariabelen in de Docker container (en dus app).

Er zijn twee van deze bestanden nodig, één voor de Django-applicatie en één voor de MariaDb database.

##### MariaDb omgevingsvariabelen

Dit bestand moet, indien je de commando's klak overneemt, volgend pad hebben "2019-2020-Stage-Blog/container/mariadb/.env". 

    MYSQL_ROOT_PASSWORD=supergeheimpaswoordtotaalnietAZERTY123
    MYSQL_DATABASE=stageblog
    MYSQL_USER=client
    MYSQL_PASSWORD=clientgeheimpwAZERTY123

##### Django omgevingsvariabelen 

Dit bestand moet, indien je de commando's klak overneemt, volgend pad hebben "2019-2020-Stage-Blog/container/app/.env". 

    MYSQL_PASSWORD=clientgeheimpwAZERTY123
    MYSQL_PORT=3306
    MYSQL_DB_NAME=stageblog
    MYSQL_USER=client
    MYSQL_HOST=stage_blog_db
    DEBUG=0
    SECRET_KEY=MOET_HOGE_ENTROPIE_HEBBEN

#### Docker containerization

---
***TIP***

Een niet-standaard bridged Docker netwerk opzetten zorgt ervoor dat de onderlinge containers (en dus applicaties) met elkaar kunnen communiceren op een DSN-like manier, bij naam dus.

---

##### Netwerk aanmaken

    # by default the network driver type is 'bridged'
    $ sudo docker network create stage_blog_net

##### Database Container

In een productie-omgeving is het sterk af te raden om SQLite3 te gebruiken. SQLite3 werkt enkel sequentieel waardoor een bottleneck al snel gevormd kan worden.

    # cd into '2019-2019-Stage-Blog'
    $ sudo docker run --name stage_blog_db --network stage_blog_net --mount type=volume,source=mariadb_vol,destination=/var/lib/mysql,volume-label="color=blue",volume-label="shape=round" --detach --env-file ./container/mariadb/.env mariadb

Vergeet niet in de juiste folder te zijn vooraleer je de container aanmaakt, anders kan het bestand met de environment variabelen niet gevonden worden.

##### Nginx Reverse Proxy

Nginx wordt niet in een container gestoken, persoonlijk zie ik geen nut in dit via een container te doen.
Wanneer je meer dan 1 service moet aanbieden is het niet ongewoon dat je meerdere Nginx containers zou laten draaien of dat de Nginx container in meerdere Docker netwerken zit. Kortom het maakt het een onnodige warreboel.

Om Django in productie te gebruiken is het aangeraden om het leveren van statische bestanden (CSS, JavaScript) over te laten aan een webserver zoals Nginx of Apache. 
Om Nginx deze bestanden te laten leveren moet enige configuratie gebeuren.

    $ sudo apt install -y nginx
    $ sudo mkdir -p /var/www/blog.vincentbockaert.xyz/static 
    # this is where the files will be hosted
    # Django container points STATIC_URL to this
    # see STATIC_ROOT in settings.py
    $ sudo chown -R $USER:$USER /var/www/blog.vincentbockaert.xyz/static
    $ sudo chmod 755 -R /var/www/blog.vincentbockaert.xyz/static
    # run from same directory as manage.py
    $ python manage.py collectstatic # will collect all static files

Nginx zelf heeft ook enige configuratie nodig, maak hiervoor volgend bestand aan **/etc/nginx/sites-available/blog.vincentbockaert.xyz**, met volgende inhoud:

---

    upstream stageblog {
	    server localhost:5000;
    }   


    server  {
	    listen 80;
	    listen [::]:80;
	    server_name blog.vincentbockaert.xyz www.blog.vincentbockaert.xyz;

	    # proxy dynamic content to the backend application (django in this instance)
	    location / {
		    proxy_pass http://stageblog;
		    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		    proxy_set_header Host $host;
		    proxy_redirect off;
	    }

    	location /static/ {
		    alias /var/www/blog.vincentbockaert.xyz/static/;
	    }
    }

---

Vergeet niet deze configuratie bekend te maken aan Nginx:

    $ cd /etc/nginx/sites-enabled
    $ sudo ln -s /etc/nginx/sites-available/blog.vincentbockaert.xyz # creërt een symbolische link waardoor de config ook in sites-enabled "zit"
    $ ls -l

Last but not least (and often forgotten), herstart nginx zodat het deze configuratie kan opnemen.

    sudo nginx -t # tests the config for errors
    sudo systemctl restart nginx

Surf nu naar je website of je publieke IP ...


##### Django Container

De Django container is gebaseerd op Debian Buster.
Een mogelijk addertje onder het gras is de **ALLOWED_HOSTS** instelling in settings.py, standaard laat die enkel localhost, 127.0.0.1 en blog.vincentbockaert.xyz toe, indien je een eigen DNS-naam gebruikt moet je dit aanpassen vooraleer je de container bouwt.
Dit moet je uiteraard ook aanpassen in je Nginx configuratie, uiteraard moet je ook de nodige records aangemaakt die naar je webserver pointen (dit lijkt mij echter evident).

    # cd into '2019-2019-Stage-Blog'
    $ sudo docker image build -f ./container/app/Dockerfile -t stage_blog_im:latest .
    $ sudo docker container run --publish 5000:8000 --detach --network stage_blog_net --name stage_blog_app --env-file ~/2019-2020-Stage-Blog/container/app/.env stage_blog_im
    sudo docker exec stage_django_blog_cont python manage.py migrate --noinput

Controleer als alle containers _OK_ zijn via `sudo docker container ls -a`.







