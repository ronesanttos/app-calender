# 📅 App Calender

Sistema web de calendário/agenda com Django, permitindo criar, editar e visualizar eventos, focado em organização, segurança e boa experiência do usuário.

---

## 🚀 Funcionalidades

- Visualização de compromissos em formato de calendário
- Interface interativa com **FullCalendar**
- Autenticação segura utilizando **JWT**
- Persistência de dados com **MongoDB via MongoEngine**
- Organização de compromissos por datas
- Estrutura preparada para integrações e expansões futuras

---

## 🛠️ Tecnologias Utilizadas

### Back-end
- **Python**
- **Django**
- **MongoEngine**
- **MongoDB**
- **JWT (JSON Web Token)**

### Front-end
- **HTML5**
- **CSS3**
- **JavaScript**
- **FullCalendar.js**

---

## 📂 Estrutura do Projeto
app-calender/
│
├── manage.py
├── requirements.txt
├── project/
│ └── settings.py
├── home/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── templates/
├── base_templates/
├── static/
└── db.sqlite3

## ⚙️ Como Rodar o Projeto Localmente

1. `git clone ...`
2. `cd app-calender`
3. `python -m venv venv`
4. `pip install -r requirements.txt`
5. `python manage.py migrate`
6. `python manage.py runserver`
7. 
