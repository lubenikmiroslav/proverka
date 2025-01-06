# Použij oficiální obraz Node.js jako základ
FROM node:14

# Instaluj Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Nastav pracovní adresář v kontejneru
WORKDIR /usr/src/app

# Zkopíruj package.json a package-lock.json (pokud existuje)
COPY package*.json ./

# Nainstaluj Node.js závislosti
RUN npm install

# Zkopíruj requirements.txt a nainstaluj Python závislosti
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Zkopíruj zbytek zdrojového kódu aplikace
COPY . .

# Exponuj port, na kterém aplikace poběží
EXPOSE 3000

# Definuj příkaz pro spuštění aplikace
CMD ["python3", "app.py"]
