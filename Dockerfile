# Použij oficiální obraz Node.js jako základ
FROM node:14

# Nastav pracovní adresář v kontejneru
WORKDIR /usr/src/app

# Zkopíruj package.json a package-lock.json (pokud existuje)
COPY package*.json ./

# Nainstaluj závislosti
RUN npm install

# Zkopíruj zbytek zdrojového kódu aplikace
COPY . .

# Zkopíruj app.py do pracovního adresáře
COPY app.py .

# Exponuj port, na kterém aplikace poběží
EXPOSE 3000

# Definuj příkaz pro spuštění aplikace
CMD ["python", "app.py"]